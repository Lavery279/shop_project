from django.contrib import admin
from .models import Product, Category
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.urls import reverse
from unfold.sections import TableSection


class CustomTableSection(TableSection):
    verbose_name = "Продукти"
    height = 300
    related_name = "products"
    fields = ["pk", "title", "price", "count"]


@admin.register(Product)
class ProductAdmin(ModelAdmin):

    def category_preview(self, obj):
        return format_html("<a href='{}'>{}</a>", reverse("admin:catalog_category_change", args=[obj.category.id]), obj.category.name)

    def reviews_preview(self, obj):
        return obj.reviews.count()

    list_display = ["title", "price", "category_preview", "count", "description", "reviews_preview"]
    ordering = ["title", "price"]
    list_filter = ["category"]
    search_fields = ["title", "description"]
    list_editable = ["price", "count"]

    category_preview.short_description = "Категорія"

    compressed_fields = True
    list_filter_sheet = False


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    def count_products(self, obj):
        return obj.products.count()
    count_products.short_description = "Кількість продуктів"
    list_display = ["name", "count_products"]
    list_sections = [CustomTableSection]
