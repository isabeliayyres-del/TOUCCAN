"""
Comando para criar métodos de pagamento iniciais
Uso: python manage.py create_payment_methods
"""
from django.core.management.base import BaseCommand
from transactions.models import PaymentMethod


class Command(BaseCommand):
    help = 'Cria métodos de pagamento iniciais'

    def handle(self, *args, **options):
        payment_methods = [
            {'name': 'Cartão de Crédito', 'description': 'Pagamento com cartão de crédito'},
            {'name': 'Cartão de Débito', 'description': 'Pagamento com cartão de débito'},
            {'name': 'PIX', 'description': 'Pagamento via PIX'},
            {'name': 'Boleto', 'description': 'Pagamento via boleto bancário'},
        ]

        for method_data in payment_methods:
            method, created = PaymentMethod.objects.get_or_create(
                name=method_data['name'],
                defaults=method_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Método de pagamento "{method.name}" criado com sucesso!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Método de pagamento "{method.name}" já existe.')
                )

