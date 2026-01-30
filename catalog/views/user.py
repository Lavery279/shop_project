from django.shortcuts import render, redirect
from catalog.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from catalog.models import Order


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            form.add_error(None, "Невірний email або пароль")

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


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "catalog/profile.html", {"orders": orders})
