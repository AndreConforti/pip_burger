from decimal import Decimal
from django.db import models


class Table(models.Model):
    """
    Representa uma mesa física na lanchonete e seu estado atual.
    """
    STATUS_CHOICES = [
        ('available', 'Livre'),
        ('occupied', 'Ocupada'),
        ('bill', 'Pediu a Conta'),
        ('reserved', 'Reservada'),
        ('joined', 'Mesa Unida'),
    ]

    number = models.IntegerField(unique=True)
    capacity = models.IntegerField(default=4)
    current_customers = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    linked_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='joined_tables')

    def __str__(self):
        """
        Retorna a representação em string da mesa.
        """
        return f"Mesa {self.number}"

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ['number']

    @property
    def total_consumption(self):
        """
        Calcula o valor total de consumo da mesa somando todas as suas comandas ativas.
        
        Busca ordens com status 'open' (aberta) ou 'closing' (conta solicitada).
        A soma é feita em Python para garantir que as properties de cálculo do 
        modelo Order sejam respeitadas.
        """
        # Filtra as comandas ativas vinculadas a esta mesa
        active_orders = self.orders.filter(status__in=['open', 'closing'])
        
        # Soma o total_value de cada comanda
        total = sum(order.total_value for order in active_orders)
        
        # Retorna o valor formatado como Decimal para evitar erros de precisão
        return Decimal(total).quantize(Decimal("0.00"))