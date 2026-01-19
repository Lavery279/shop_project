from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва категорії")

    def get_absolute_url(self):
        return reverse("category", args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Product(models.Model):
    external_id = models.CharField(unique=True, verbose_name="Зовнішній ID", max_length=255)
    title = models.CharField(max_length=255, verbose_name="Назва продукту")
    description = models.TextField(verbose_name="Опис продукту")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",   verbose_name="Категорія")
    image = models.CharField(max_length=512, null=True, blank=True, verbose_name="Зображення")
    count = models.IntegerField(default=0, verbose_name="Кількість на складі")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"
