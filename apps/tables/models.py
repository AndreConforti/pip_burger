from decimal import Decimal
from django.db import models

class Table(models.Model):
    """
    Representa uma mesa física na lanchonete e seu estado atual.
    
    A lógica de mesas permite o vínculo (self-reference) onde uma mesa 'filha' 
    pode ser vinculada a uma mesa 'mestra' através do campo linked_to. 
    Nestes casos, a mesa filha herda comportamentos financeiros e de status da mestra.
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
    linked_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='joined_tables'
    )

    def __str__(self):
        return f"Mesa {self.number}"

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ['number']

    def get_effective_status(self):
        """
        Retorna o status operacional real da mesa.
        Se a mesa estiver vinculada a uma mestra, ela assume o status da mestra 
        (ex: se a mestra pediu a conta, a vinculada também aparece como 'Pediu a Conta').
        Caso contrário, retorna seu próprio status.
        """
        if self.linked_to:
            return self.linked_to.status
        return self.status

    def join_with(self, master_table):
        """
        Realiza o vínculo técnico entre duas mesas.
        A mesa atual (filha) passa a apontar para a master_table (mestra).
        Automaticamente altera o status da filha para 'occupied'.
        """
        if master_table != self:
            self.linked_to = master_table
            self.status = 'occupied' 
            self.save()

    @property
    def individual_consumption(self):
        """
        Calcula a soma monetária apenas das comandas (Order) vinculadas diretamente 
        a esta mesa específica que estejam com status 'open' ou 'closing'.
        """
        active_orders = self.orders.filter(status__in=['open', 'closing'])
        total = sum(order.total_value for order in active_orders)
        return Decimal(total).quantize(Decimal("0.00"))

    @property
    def linked_consumption(self):
        """
        Percorre todas as mesas vinculadas a esta (joined_tables) e soma o 
        individual_consumption de cada uma. Utilizado apenas por mesas Mestras.
        """
        total = Decimal('0.00')
        for linked_table in self.joined_tables.all():
            total += linked_table.individual_consumption
        return total.quantize(Decimal("0.00"))

    @property
    def total_consumption(self):
        """
        Calcula o valor total visível para a mesa no frontend.
        - Se for uma mesa mestra ou solitária: Soma o consumo próprio + consumo das filhas.
        - Se for uma mesa vinculada: Retorna apenas seu próprio consumo para 
          evitar redundância visual de valores, já que o total será pago na mestra.
        """
        if self.linked_to:
            return self.individual_consumption
            
        return (self.individual_consumption + self.linked_consumption).quantize(Decimal("0.00"))