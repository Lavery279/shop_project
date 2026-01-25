from django.shortcuts import render
from catalog.models import Product


def home(request):
    products = Product.objects.all()[:8]

    return render(request, "catalog/index.html", {"products": products})
