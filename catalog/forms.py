from django import forms
from .models import Review, Order
import re


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Невірний логін або пароль.")
            else:
                cleaned_data["user"] = user

        return cleaned_data


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Підтвердження паролю"
    )

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
            "rating": forms.RadioSelect(choices=[(i, "★" * i) for i in range(1, 6)]),
            "comment": forms.Textarea(attrs={"rows": 4}),
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
