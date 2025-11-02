# carts/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem, Payment
from products.serializers import ProductSerializer
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'cart_id']
        read_only_fields = ['id', 'product', 'cart_id']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'created_at', 'updated_at', 'is_active', 'items', 'total']
        read_only_fields = ['id', 'created_at', 'updated_at', 'items', 'total']

    def get_total(self, obj):
        return obj.total()

class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

class CheckoutSerializer(serializers.Serializer):
    payment_method = serializers.CharField(max_length=50, default='dummy')
    # TO DO -> Adicionar endereco
