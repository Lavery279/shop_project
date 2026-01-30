from django.shortcuts import render, redirect
from catalog.models import OrderItem, OrderStatus
from .cart import Cart
from django.contrib import messages
from catalog.forms import CheckoutForm


def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.status = OrderStatus.objects.get(code="pending")
            order.save()

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
        else:
            return render(
                request,
                "catalog/checkout.html",
                {
                    "cart": cart,
                    "cart_total": sum(item["total"] for item in cart),
                    "form": form,
                },
            )

    return render(
        request,
        "catalog/checkout.html",
        {
            "cart": cart,
            "cart_total": sum(item["total"] for item in cart),
            "form": CheckoutForm(),
        },
    )
