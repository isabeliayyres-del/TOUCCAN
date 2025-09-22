from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
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

    fieldsets = (
        ("Informações básicas", {
            "fields": ("name", "description", "parent")
        }),
        ("Configurações", {
            "fields": ("slug", "is_active")
        }),       
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'seller', 'price', 'stock_quantity', 'is_active', 'featured', 'created_at')
    list_filter = ('category', 'is_active', 'featured', 'created_at', 'seller')
    search_fields = ('title', 'description', 'seller__username')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'featured', 'price', 'stock_quantity')
    ordering = ('-created_at',)
    inlines = [ProductImageInline]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description', 'category', 'seller')
        }),
        ('Preço e Estoque', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Configurações', {
            'fields': ('slug', 'is_active', 'featured')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'seller')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__title', 'alt_text')
    list_editable = ('is_primary', 'order')
    ordering = ('product', 'order')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')
