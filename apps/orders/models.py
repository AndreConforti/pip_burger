from decimal import Decimal
from django.db import models
from django.db.models import Sum, F
from apps.tables.models import Table
from apps.menu.models import Product


class Order(models.Model):
    """
    Representa uma comanda ou pedido vinculado a uma mesa.
    Uma mesa pode ter múltiplos pedidos ativos (rateio/comandas individuais).
    """
    STATUS_CHOICES = [
        ('open', 'Aberta'),
        ('closing', 'Aguardando Pagamento'),
        ('paid', 'Paga'),
        ('cancelled', 'Cancelada'),
    ]

    table = models.ForeignKey(
        Table, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name="Mesa"
    )
    customer_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Nome do Cliente"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='open'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_value(self):
        """
        Calcula o valor bruto total da comanda.
        
        Soma o resultado de (quantidade * preço_unitario) para cada item vinculado.
        Retorna: decimal.Decimal (0.00 caso não existam itens).
        """
        total = self.items.aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )['total']
        return total if total is not None else Decimal("0.00")

    @property
    def total_paid(self):
        """
        Calcula o montante total já amortizado por pagamentos realizados.
        
        Soma todos os registros na tabela Payment vinculados a este pedido.
        Retorna: decimal.Decimal (0.00 caso não existam pagamentos).
        """
        paid = self.payments.aggregate(
            total=Sum('amount')
        )['total']
        return paid if paid is not None else Decimal("0.00")

    @property
    def balance_due(self):
        """
        Calcula o saldo devedor remanescente para quitação da comanda.
        
        Subtrai o total pago do valor bruto total. 
        Utilizado para determinar se a mesa pode ser liberada (saldo == 0).
        Retorna: decimal.Decimal.
        """
        return self.total_value - self.total_paid

    def __str__(self):
        """
        Retorna a identificação da comanda com o valor total.
        """
        customer = self.customer_name if self.customer_name else "Geral"
        return f"Pedido {self.id} - Mesa {self.table.number} (R$ {self.total_value})"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class OrderItem(models.Model):
    """
    Representa cada item individual dentro de uma comanda.
    Relaciona um produto a um pedido com uma quantidade e preço congelado.
    """
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Pedido"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        verbose_name="Produto"
    )
    quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name="Quantidade"
    )
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço Unitário"
    )
    observations = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Observações (ex: sem cebola)"
    )

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def save(self, *args, **kwargs):
        """
        Sobrescreve o salvamento para automatizar a busca de preço.
        
        Busca o preço atual do produto no menu caso o preço unitário 
        não tenha sido informado manualmente.
        """
        if not self.unit_price and self.product:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    Registra os pagamentos efetuados para um pedido.
    Suporta múltiplos pagamentos para a mesma comanda (rateio).
    """
    PAYMENT_METHODS = [
        ('cash', 'Dinheiro'),
        ('credit', 'Cartão de Crédito'),
        ('debit', 'Cartão de Débito'),
        ('pix', 'PIX'),
    ]

    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='payments',
        verbose_name="Pedido"
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor Pago"
    )
    method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS, 
        verbose_name="Forma de Pagamento"
    )
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"R$ {self.amount} - {self.get_method_display()}"

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
