from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from django.db.models import Avg, Count


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва категорії")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Слаг")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Зовнішній ID",
    )

    title = models.CharField(max_length=255, verbose_name="Назва продукту")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категорія",
    )
    description = models.TextField(verbose_name="Опис продукту")
    image = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="Зображення"
    )
    count = models.IntegerField(default=0, verbose_name="Кількість на складі")

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    def rating_count(self):
        return self.reviews.aggregate(count=Count("id"))["count"] or 0

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} — {self.rating}"


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    delivery_method = models.CharField(
        max_length=50,
        choices=[
            ("nova-poshta", "Нова Пошта"),
            ("courier", "Кур’єр"),
        ],
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("card", "Картка"),
            ("cash", "Накладений платіж"),
        ],
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення #{self.id} від {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price
