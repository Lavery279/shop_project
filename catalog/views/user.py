from django.shortcuts import render, redirect
from catalog.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from catalog.models import Order


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        login(request, user)
        return redirect("profile")

    return render(
        request,
        "catalog/auth.html",
        {"form": form, "is_login": True, "is_submitting": request.method == "POST"},
    )


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        login(request, user)

        return redirect("profile")

    return render(
        request,
        "catalog/auth.html",
        {"form": form, "is_login": False, "is_submitting": request.method == "POST"},
    )


def logout_view(request):
    logout(request)
    return redirect("home")


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    orders = Order.objects.filter(user=request.user).order_by("-created")
    return render(request, "catalog/profile.html", {"orders": orders})
