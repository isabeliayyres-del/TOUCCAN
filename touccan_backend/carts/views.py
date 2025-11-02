from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Cart, CartItem, Payment
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, CheckoutSerializer
from products.models import Product
from orders.models import Order, OrderItem  # assume OrderItem model exists and named so
from users.models import User

class CartViewSet(viewsets.GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        # Se usuario autenticado, filtra pelo usuário
        # user = getattr(self.request, 'user', None)
        # if user and user.is_authenticated:
        #     return Cart.objects.filter(user=user)
        # Caso sem auth, permitir ver todos (ou aplicar outra regra)
        return Cart.objects.all()

    def list(self, request):
        user = request.user if request.user.is_authenticated else None
        if user:
            cart, _ = Cart.objects.get_or_create(user=user, is_active=True)
            serializer = CartSerializer(cart, context={'request': request})
            return Response(serializer.data)
        return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False, url_path='add')
    def add_item(self, request):
        """
        payload: { "product_id": 123, "quantity": 2 }
        """
        user = request.user if request.user.is_authenticated else None
        if not user:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, pk=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        cart, _ = Cart.objects.get_or_create(user=user, is_active=True)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartSerializer(cart, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='remove')
    def remove_item(self, request):
        """
        payload: { "product_id": 123 }
        """
        user = request.user if request.user.is_authenticated else None
        if not user:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get('product_id')
        if product_id is None:
            return Response({"detail": "product_id required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, user=user, is_active=True)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response(CartSerializer(cart, context={'request': request}).data)

    @action(methods=['patch'], detail=False, url_path='update')
    def update_item(self, request):
        """
        payload: { "product_id": 123, "quantity": 3 }
        """
        user = request.user if request.user.is_authenticated else None
        if not user:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        if product_id is None or quantity is None:
            return Response({"detail": "product_id and quantity required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, user=user, is_active=True)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.quantity = int(quantity)
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()
        return Response(CartSerializer(cart, context={'request': request}).data)

    @action(methods=['post'], detail=False, url_path='checkout')
    def checkout(self, request):
        """
        Finaliza o carrinho:
        - cria Order
        - cria OrderItems copiados do CartItems (captura price atual)
        - cria Payment (simulado)
        - desativa cart
        """
        user = request.user if request.user.is_authenticated else None
        if not user:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_method = serializer.validated_data.get('payment_method', 'dummy')

        cart = get_object_or_404(Cart, user=user, is_active=True)
        items = list(cart.items.select_related('product').all())
        if not items:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # calcular total
            total = sum((item.product.price or 0) * item.quantity for item in items)

            # criar order
            order = Order.objects.create(user=user, status='pending')
            # criar order items - assumindo model OrderItem com fields: order, product, quantity, price(optional)
            order_items = []
            for item in items:
                # Se o model OrderItem tiver campo price, use item.product.price; adapt if not
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            # criar payment (simulado)
            payment = Payment.objects.create(order=order, payment_method=payment_method, amount=total, status='paid')

            # desativar cart
            cart.is_active = False
            cart.save()

        # serializar resposta mínima
        return Response({
            "order_id": order.id,
            "order_status": order.status,
            "payment_id": payment.id,
            "payment_status": payment.status,
            "total": str(payment.amount)
        }, status=status.HTTP_201_CREATED)
