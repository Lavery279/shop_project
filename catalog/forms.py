from django import forms
from .models import Review


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Підтвердження паролю"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Паролі не співпадають")
        return cleaned_data


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
