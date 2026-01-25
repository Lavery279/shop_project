from django.urls import path
from catalog.views.home import home
from catalog.views.product import catalog_view, product_list, product_detail
from catalog.views.about import about_view, contacts_view
from catalog.views.cart import add_to_cart, cart_detail, remove_from_cart, update_cart
from catalog.views.order import checkout, order_success

urlpatterns = [
    path("", home, name="home"),
    path("products/", product_list, name="product_list"),
    path("products/<uuid:pk>/", product_detail, name="product_detail"),
    path("about/", about_view, name="about"),
    path("contacts/", contacts_view, name="contacts"),
    path("cart/add/<uuid:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_detail, name="cart_detail"),
    path("checkout/", checkout, name="checkout"),
    path("order-success/<int:order_id>/", order_success, name="order_success"),
    path("cart/remove/<uuid:product_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/update/<uuid:product_id>/", update_cart, name="update_cart"),
    path("products/", catalog_view, name="catalog"),
]
