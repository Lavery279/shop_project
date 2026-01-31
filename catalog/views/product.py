from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Product, Category
from django.core.paginator import Paginator
from catalog.forms import ReviewForm


def catalog_view(request):
    products = Product.objects.all()
    search = request.GET.get("search")
    category = request.GET.get("category")
    sort = request.GET.get("sort")

    if search and len(search) >= 3:
        products = products.filter(title__icontains=search)

    if category:
        products = products.filter(category__slug=category)

    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "new":
        products = products.order_by("-created_at")

    paginator = Paginator(products, 16)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(
        request,
        "catalog/product_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "sort": sort,
            "search": search,
            "category": category,
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by("-created")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ReviewForm()

    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "form": form,
            "average_rating": product.average_rating(),
            "rating_count": product.rating_count(),
        },
    )
