from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImage(admin.TabularInline):
    model = ProductImage
    extra = 1 
    fields = ("image", "alt_text", "is_primary", "order")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    list_filter = ("is_active", "parent", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active",)
    ordering = ("name",)

    