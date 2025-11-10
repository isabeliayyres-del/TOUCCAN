from rest_framework import serializers
from .models import Transaction, PaymentMethod, TransactionStatus


class PaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer para métodos de pagamento"""
    
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer para transações"""
    payment_method_name = serializers.CharField(source='payment_method.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'transaction_id',
            'order_id',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_document',
            'payment_method',
            'payment_method_name',
            'amount',
            'currency',
            'status',
            'status_display',
            'description',
            'metadata',
            'payment_gateway_response',
            'payment_gateway_transaction_id',
            'created_at',
            'updated_at',
            'processed_at',
        ]
        read_only_fields = [
            'id',
            'transaction_id',
            'created_at',
            'updated_at',
            'processed_at',
            'payment_gateway_response',
        ]

    def validate_amount(self, value):
        """Valida que o valor é positivo"""
        if value <= 0:
            raise serializers.ValidationError("O valor deve ser maior que zero.")
        return value

    def validate_status(self, value):
        """Valida o status"""
        if value not in [choice[0] for choice in TransactionStatus.choices]:
            raise serializers.ValidationError("Status inválido.")
        return value


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de transações"""
    
    class Meta:
        model = Transaction
        fields = [
            'order_id',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_document',
            'payment_method',
            'amount',
            'currency',
            'description',
            'metadata',
        ]

    def validate_amount(self, value):
        """Valida que o valor é positivo"""
        if value <= 0:
            raise serializers.ValidationError("O valor deve ser maior que zero.")
        return value

    def create(self, validated_data):
        """Cria uma nova transação com transaction_id único"""
        import uuid
        from django.utils import timezone
        
        # Gera um transaction_id único
        transaction_id = f"TXN-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Garante que o transaction_id é único
        while Transaction.objects.filter(transaction_id=transaction_id).exists():
            transaction_id = f"TXN-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        validated_data['transaction_id'] = transaction_id
        validated_data['status'] = TransactionStatus.PENDING
        
        return super().create(validated_data)


class TransactionUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de transações"""
    
    class Meta:
        model = Transaction
        fields = [
            'status',
            'payment_gateway_response',
            'payment_gateway_transaction_id',
            'metadata',
        ]

    def validate_status(self, value):
        """Valida o status"""
        if value not in [choice[0] for choice in TransactionStatus.choices]:
            raise serializers.ValidationError("Status inválido.")
        return value


class TransactionStatusUpdateSerializer(serializers.Serializer):
    """Serializer para atualização apenas do status"""
    status = serializers.ChoiceField(choices=TransactionStatus.choices)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)

