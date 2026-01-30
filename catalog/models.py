from django.conf import settings
from django.db import models
from django.urls import reverse
import uuid
from django.db.models import Avg, Count
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Зовнішній ID",
    )
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Користувач",
    )
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} — {self.rating}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Користувач",
    )

    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    city = models.CharField(max_length=100, verbose_name="Місто")
    address = models.CharField(max_length=255, verbose_name="Адреса")
    delivery_method = models.CharField(
        max_length=50,
        choices=[
            ("nova-poshta", "Нова Пошта"),
            ("courier", "Кур’єр"),
        ],
        verbose_name="Метод доставки",
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("card", "Картка"),
            ("cash", "Накладений платіж"),
        ],
        verbose_name="Метод оплати",
    )
    status = models.ForeignKey(
        "OrderStatus",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Статус",
        default="a06eb166f8b042d8b0f5e291153f1293",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"Замовлення #{self.id} від {self.first_name} {self.last_name}"

    def total_amount(self):
        return sum(item.get_total() for item in self.items.all())

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"


class OrderStatus(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Зовнішній ID",
    )
    code = models.CharField(max_length=50, unique=True, verbose_name="Код статусу")
    label = models.CharField(max_length=100, verbose_name="Назва статусу")

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Статус замовлення"
        verbose_name_plural = "Статуси замовлень"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="Замовлення"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.PositiveIntegerField(verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    class Meta:
        verbose_name = "Товар у замовленні"
        verbose_name_plural = "Товари у замовленні"
