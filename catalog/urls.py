from django.urls import path
from catalog.views.product import product_list, product_detail

urlpatterns = [
    path("products/", product_list, name="product_list"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
]
