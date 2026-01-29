from django.shortcuts import redirect, get_object_or_404, render
from catalog.models import Product
from django.views.decorators.http import require_POST


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for product_id, item in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue
            yield {
                "product": Product.objects.get(id=product_id),
                "quantity": item["quantity"],
                "price": item["price"],
                "total": float(item["price"]) * item["quantity"],
            }

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity
            self.save()

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def is_empty(self):
        return len(self.cart) == 0

    def get_total_price(self):
        return sum(
            float(item["price"]) * item["quantity"] for item in self.cart.values()
        )


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(
        request,
        "catalog/cart.html",
        {
            "cart": cart,
            "total": cart.get_total_price(),
        },
    )


@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


@require_POST
def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart.update(product, quantity)
        else:
            cart.remove(product)
    except ValueError:
        pass
    return redirect("cart_detail")
