from django import forms
from .models import Review, Order, CustomUser
import re
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            if not CustomUser.objects.filter(username=email).exists():
                raise forms.ValidationError("Користувача з такою поштою не знайдено.")

            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Невірний пароль.")
            cleaned_data["user"] = user

        return cleaned_data


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise forms.ValidationError("Email має бути у форматі name@example.com")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 6:
            raise forms.ValidationError("Пароль має містити щонайменше 6 символів.")

        if not re.search(r"[A-Za-z]", password):
            raise forms.ValidationError("Пароль має містити хоча б одну літеру.")

        if not re.search(r"\d", password):
            raise forms.ValidationError("Пароль має містити хоча б одну цифру.")

        return password


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.RadioSelect(
                choices=[(i, "★" * i) for i in range(1, 6)],
                attrs={"class": "flex gap-2"},
            ),
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 25,
                    "class": "w-full resize-none rounded-lg border border-gray-300 p-3 text-sm focus:ring-2 focus:ring-primary",
                }
            ),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating not in range(1, 6):
            raise forms.ValidationError("Оцінка повинна бути від 1 до 5.")
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get("comment", "").strip()
        if not comment:
            raise forms.ValidationError("Коментар не може бути порожнім.")
        if len(comment) < 5:
            raise forms.ValidationError("Коментар має містити щонайменше 5 символів.")
        return comment

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get("rating")
        comment = cleaned_data.get("comment")

        if rating == 1 and len(comment) < 20:
            self.add_error(
                "comment", "Для оцінки 1 бажано написати детальніший коментар."
            )
        return cleaned_data


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "city",
            "address",
            "delivery_method",
            "payment_method",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise forms.ValidationError("Email має бути у форматі name@example.com")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = r"^\+380 \d{2}-\d{3}-\d{4}$"
        if not re.match(pattern, phone):
            raise forms.ValidationError("Телефон має бути у форматі +380 XX-XXX-XXXX")
        return phone
