from django.shortcuts import render, redirect
from catalog.models import Order, OrderItem
from .cart import Cart
from django.contrib import messages


def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("cart_detail")

    if request.method == "POST":
        order = Order.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            city=request.POST.get("city"),
            address=request.POST.get("address"),
            delivery_method=request.POST.get("delivery_method"),
            payment_method=request.POST.get("payment_method"),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
            )

        cart.clear()

        messages.success(request, "Дякуємо за замовлення!")
        return redirect("cart_detail")

    return render(
        request,
        "catalog/checkout.html",
        {
            "cart": cart,
            "cart_total": sum(item["total"] for item in cart),
        },
    )
