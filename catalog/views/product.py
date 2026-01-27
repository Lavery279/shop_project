from django.shortcuts import render, get_object_or_404
from ..models import Product, Category


def product_list(request):
    products = Product.objects.all()
    sort = request.GET.get("sort")

    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "new":
        products = products.order_by("-created_at")

    return render(request, "catalog/product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def catalog_view(request):
    products = Product.objects.all()
    search = request.GET.get("search")
    category = request.GET.get("category")
    sort = request.GET.get("sort")

    if search:
        products = products.filter(title__icontains=search)

    if category:
        products = products.filter(category__slug=category)

    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "new":
        products = products.order_by("-created_at")

    categories = Category.objects.all()
    return render(
        request,
        "catalog/product_list.html",
        {
            "products": products,
            "categories": categories,
        },
    )
