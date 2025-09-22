from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'parent', 'slug', 
            'is_active', 'created_at', 'updated_at',
            'subcategories', 'full_path', 'products_count'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_subcategories(self, obj):
        subcategories = obj.get_children()
        return CategorySerializer(subcategories, many=True, context=self.context).data

    def get_full_path(self, obj):
        return obj.get_full_path()

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class CategoryListSerializer(serializers.ModelSerializer):
    full_path = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'parent', 'slug', 'is_active',
            'full_path', 'products_count'
        ]

    def get_full_path(self, obj):
        return obj.get_full_path()

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            'id', 'image', 'image_url', 'alt_text', 
            'is_primary', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_path = serializers.SerializerMethodField()
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    primary_image = serializers.SerializerMethodField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'stock_quantity',
            'category', 'category_name', 'category_path', 'seller',
            'seller_username', 'slug', 'is_active', 'featured',
            'created_at', 'updated_at', 'images', 'primary_image',
            'is_in_stock'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'seller']

    def get_category_path(self, obj):
        return obj.category.get_full_path()

    def get_primary_image(self, obj):
        primary_image = obj.primary_image
        if primary_image:
            return ProductImageSerializer(primary_image, context=self.context).data
        return None

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'stock_quantity', 'category_name',
            'seller_username', 'slug', 'is_active', 'featured',
            'created_at', 'primary_image'
        ]

    def get_primary_image(self, obj):
        primary_image = obj.primary_image
        if primary_image and primary_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price', 'stock_quantity',
            'category', 'is_active', 'featured'
        ]

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("A quantidade em estoque não pode ser negativa.")
        return value



