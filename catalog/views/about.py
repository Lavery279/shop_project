from django.shortcuts import render


def about_view(request):
    return render(request, "catalog/about.html")


def contacts_view(request):
    return render(request, "catalog/contacts.html")
