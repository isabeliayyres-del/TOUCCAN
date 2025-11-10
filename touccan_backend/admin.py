from django.contrib import admin
from .models import Transaction, PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 
        'order_id', 
        'customer_name', 
        'amount', 
        'status', 
        'payment_method',
        'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['transaction_id', 'order_id', 'customer_name', 'customer_email']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('transaction_id', 'order_id', 'status')
        }),
        ('Cliente', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_document')
        }),
        ('Pagamento', {
            'fields': ('payment_method', 'amount', 'currency')
        }),
        ('Informações Adicionais', {
            'fields': ('description', 'metadata')
        }),
        ('Gateway de Pagamento', {
            'fields': ('payment_gateway_transaction_id', 'payment_gateway_response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at')
        }),
    )

