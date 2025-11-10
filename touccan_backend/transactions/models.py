from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class PaymentMethod(models.Model):
    """Métodos de pagamento disponíveis"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Método de Pagamento'
        verbose_name_plural = 'Métodos de Pagamento'
        ordering = ['name']

    def __str__(self):
        return self.name


class TransactionStatus(models.TextChoices):
    """Status possíveis de uma transação"""
    PENDING = 'pending', 'Pendente'
    PROCESSING = 'processing', 'Processando'
    APPROVED = 'approved', 'Aprovada'
    REJECTED = 'rejected', 'Rejeitada'
    CANCELLED = 'cancelled', 'Cancelada'
    REFUNDED = 'refunded', 'Reembolsada'


class Transaction(models.Model):
    """Modelo principal de transação"""
    # Informações básicas
    transaction_id = models.CharField(max_length=100, unique=True, db_index=True)
    order_id = models.CharField(max_length=100, db_index=True, help_text='ID do pedido no sistema externo')
    
    # Informações do cliente
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_document = models.CharField(max_length=20, blank=True, help_text='CPF/CNPJ')
    
    # Informações de pagamento
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Valor da transação'
    )
    currency = models.CharField(max_length=3, default='BRL', help_text='Código da moeda (BRL, USD, etc)')
    
    # Status e controle
    status = models.CharField(
        max_length=20, 
        choices=TransactionStatus.choices, 
        default=TransactionStatus.PENDING
    )
    
    # Informações adicionais
    description = models.TextField(blank=True, help_text='Descrição da transação')
    metadata = models.JSONField(default=dict, blank=True, help_text='Dados adicionais em formato JSON')
    
    # Informações de processamento
    payment_gateway_response = models.JSONField(default=dict, blank=True, help_text='Resposta do gateway de pagamento')
    payment_gateway_transaction_id = models.CharField(max_length=200, blank=True, help_text='ID da transação no gateway')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True, help_text='Data de processamento')
    
    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['order_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.customer_name} - R$ {self.amount}"

    def mark_as_approved(self):
        """Marca a transação como aprovada"""
        self.status = TransactionStatus.APPROVED
        if not self.processed_at:
            from django.utils import timezone
            self.processed_at = timezone.now()
        self.save()

    def mark_as_rejected(self, reason=None):
        """Marca a transação como rejeitada"""
        self.status = TransactionStatus.REJECTED
        if reason:
            self.metadata['rejection_reason'] = reason
        self.save()

    def mark_as_processing(self):
        """Marca a transação como processando"""
        self.status = TransactionStatus.PROCESSING
        self.save()

