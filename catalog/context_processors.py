from .views.cart import Cart


def cart_item_count(request):
    cart = Cart(request)
    total_items = sum(item["quantity"] for item in cart)
    return {"cart_item_count": total_items}
