from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.utils import timezone
from .models import Transaction, PaymentMethod, TransactionStatus
from .serializers import (
    TransactionSerializer,
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
    TransactionStatusUpdateSerializer,
    PaymentMethodSerializer,
)


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para métodos de pagamento (somente leitura)"""
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [AllowAny]


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet para transações"""
    queryset = Transaction.objects.all()
    permission_classes = [AllowAny]  # Em produção, configure autenticação adequada
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado baseado na ação"""
        if self.action == 'create':
            return TransactionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TransactionUpdateSerializer
        return TransactionSerializer

    def get_queryset(self):
        """Filtra o queryset baseado nos parâmetros de query"""
        queryset = Transaction.objects.all()
        
        # Filtro por order_id
        order_id = self.request.query_params.get('order_id', None)
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        # Filtro por transaction_id
        transaction_id = self.request.query_params.get('transaction_id', None)
        if transaction_id:
            queryset = queryset.filter(transaction_id=transaction_id)
        
        # Filtro por status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filtro por email do cliente
        customer_email = self.request.query_params.get('customer_email', None)
        if customer_email:
            queryset = queryset.filter(customer_email=customer_email)
        
        # Filtro por data (from_date e to_date)
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        if from_date:
            queryset = queryset.filter(created_at__gte=from_date)
        if to_date:
            queryset = queryset.filter(created_at__lte=to_date)
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Aprova uma transação"""
        transaction = self.get_object()
        
        if transaction.status == TransactionStatus.APPROVED:
            return Response(
                {'error': 'Transação já está aprovada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.mark_as_approved()
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rejeita uma transação"""
        transaction = self.get_object()
        
        if transaction.status == TransactionStatus.REJECTED:
            return Response(
                {'error': 'Transação já está rejeitada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reason = request.data.get('reason', '')
        transaction.mark_as_rejected(reason=reason)
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Marca uma transação como processando"""
        transaction = self.get_object()
        
        if transaction.status == TransactionStatus.PROCESSING:
            return Response(
                {'error': 'Transação já está em processamento.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.mark_as_processing()
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Atualiza o status de uma transação"""
        transaction = self.get_object()
        serializer = TransactionStatusUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            transaction.status = new_status
            
            if new_status == TransactionStatus.APPROVED and not transaction.processed_at:
                transaction.processed_at = timezone.now()
            
            if new_status == TransactionStatus.REJECTED:
                reason = serializer.validated_data.get('rejection_reason', '')
                if reason:
                    transaction.metadata['rejection_reason'] = reason
            
            transaction.save()
            
            return Response(TransactionSerializer(transaction).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Retorna estatísticas das transações"""
        queryset = self.get_queryset()
        
        total_transactions = queryset.count()
        total_amount = sum(t.amount for t in queryset)
        
        status_counts = {}
        for status_choice in TransactionStatus.choices:
            status_counts[status_choice[0]] = queryset.filter(status=status_choice[0]).count()
        
        return Response({
            'total_transactions': total_transactions,
            'total_amount': float(total_amount),
            'status_counts': status_counts,
        })

