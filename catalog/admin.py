from django.contrib import admin
from .models import Product, Category, Review, Order, OrderItem, OrderStatus
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.urls import reverse
from unfold.sections import TableSection


class ProductTableSection(TableSection):
    verbose_name = "Продукти"
    height = 300
    related_name = "products"
    fields = ["pk", "title", "price", "count"]


@admin.register(Product)
class ProductAdmin(ModelAdmin):

    def category_preview(self, obj):
        return format_html(
            "<a href='{}'>{}</a>",
            reverse("admin:catalog_category_change", args=[obj.category.id]),
            obj.category.name,
        )

    def reviews_preview(self, obj):
        return obj.reviews.count()

    list_display = [
        "title",
        "price",
        "category_preview",
        "count",
        "description",
        "reviews_preview",
    ]
    ordering = ["title", "price"]
    list_filter = ["category"]
    search_fields = ["title", "description"]
    list_editable = ["price", "count"]

    category_preview.short_description = "Категорія"
    reviews_preview.short_description = "Відгуки"

    compressed_fields = True
    list_filter_sheet = False


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    def count_products(self, obj):
        return obj.products.count()

    count_products.short_description = "Кількість продуктів"
    list_display = ["name", "count_products"]
    list_sections = [ProductTableSection]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    def product_preview(self, obj):
        return format_html(
            "<a href='{}'>{}</a>",
            reverse("admin:catalog_product_change", args=[obj.product.id]),
            obj.product.title,
        )

    list_display = ["product_preview", "user", "rating", "comment", "created"]
    list_filter = ["rating", "created"]
    search_fields = ["comment"]

    product_preview.short_description = "Продукт"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    def total_amount_preview(self, obj):
        return f"{obj.total_amount()} ₴"

    list_display = [
        "id",
        "user",
        "first_name",
        "last_name",
        "city",
        "created",
        "total_amount_preview",
        "delivery_method",
        "payment_method",
        "status",
    ]
    list_filter = ["delivery_method", "payment_method", "created", "status"]
    search_fields = ["first_name", "last_name", "email", "city"]
    list_editable = ["status"]
    inlines = [OrderItemInline]

    total_amount_preview.short_description = "Сума"


@admin.register(OrderStatus)
class OrderStatusAdmin(ModelAdmin):
    list_display = ["code", "label"]
    search_fields = ["label"]


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    def product_preview(self, obj):
        return format_html(
            "<a href='{}'>{}</a>",
            reverse("admin:catalog_product_change", args=[obj.product.id]),
            obj.product.title,
        )

    list_display = ["order", "product_preview", "quantity", "price", "get_total"]
    list_filter = ["order", "product"]
    product_preview.short_description = "Продукт"
