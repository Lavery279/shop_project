from django.shortcuts import get_object_or_404, render, redirect
from catalog.models import Order, OrderItem
from .cart import Cart


def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        city = request.POST.get("city")
        address = request.POST.get("address")
        delivery_method = request.POST.get("delivery_method")
        payment_method = request.POST.get("payment_method")

        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            city=city,
            address=address,
            delivery_method=delivery_method,
            payment_method=payment_method,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item[
                    "product"
                ],
                quantity=item["quantity"],
                price=item["price"],
            )

        cart.clear()

        return redirect("order_success", order_id=order.id)

    return render(
        request,
        "catalog/checkout.html",
        {
            "cart": cart,
            "cart_total": sum(item["total"] for item in cart),
        },
    )


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "catalog/order_success.html", {"order": order})
