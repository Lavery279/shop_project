from django.shortcuts import render, redirect
from catalog.forms import LoginForm, RegisterForm


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # логіка входу
        return redirect("home")
    return render(
        request,
        "catalog/auth.html",
        {"form": form, "is_login": True, "is_submitting": request.method == "POST"},
    )


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # логіка реєстрації
        return redirect("home")
    return render(
        request,
        "catalog/auth.html",
        {"form": form, "is_login": False, "is_submitting": request.method == "POST"},
    )
