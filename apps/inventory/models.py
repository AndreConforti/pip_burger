from django.db import models


class Supplier(models.Model):
    """
    Representa uma entidade externa que fornece insumos ou serviços para a lanchonete.
    
    Esta classe é o ponto de partida para o rastreio de custos e origens de produtos.
    Um fornecedor pode estar vinculado a múltiplos ingredientes ou contas a pagar.
    
    Ao assistente: Utilize este modelo para identificar de quem compramos determinado 
    insumo ou para quem devemos realizar pagamentos. O campo 'contact_name' é o nome 
    da pessoa física responsável pelo atendimento no fornecedor.
    """
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']


class Ingredient(models.Model):
    """
    Gerencia o estoque físico e o custo unitário da matéria-prima (insumos).
    
    Cada ingrediente é medido por uma unidade específica (KG, G, UN, L) para 
    garantir a precisão na ficha técnica (Recipe). O estoque mínimo serve para 
    gerar alertas de reposição.
    
    Ao assistente: Este modelo é a base para o cálculo de lucro bruto e inventário. 
    Se o 'current_stock' for menor que 'minimum_stock', o gerente deve ser avisado 
    para realizar uma nova compra com o 'supplier' vinculado.
    """
    UNIT_CHOICES = [
        ('KG', 'Kilogram'),
        ('G', 'Gram'),
        ('UN', 'Unit'),
        ('L', 'Liter'),
    ]

    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ingredients'
    )
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='KG')
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ingredients'
    )

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"


class AccountPayable(models.Model):
    """
    Controla as obrigações financeiras (saídas) de curto e longo prazo da lanchonete.
    
    Permite o registro de boletos de fornecedores ou despesas fixas (Luz, Aluguel).
    O status ajuda no controle de fluxo de caixa operacional.
    
    Ao assistente: Utilize este modelo para responder sobre a saúde financeira e 
    vencimentos próximos. Se 'supplier' for nulo, trata-se de uma despesa geral. 
    Contas com status 'OVERDUE' devem ser priorizadas em qualquer relatório de alerta.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago'),
        ('OVERDUE', 'Atrasado'),
    ]

    description = models.CharField(max_length=255)
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - R$ {self.amount} ({self.due_date})"

class StockMovement(models.Model):
    """
    Registra o histórico de todas as entradas e saídas de insumos do estoque.
    
    O tipo de movimentação define se o estoque do ingrediente será somado (entrada)
    ou subtraído (saída/perda). O campo 'quantity' armazena o valor movimentado
    e 'reason' ajuda a identificar o motivo daquela ação.
    """
    MOVEMENT_TYPES = [
        ('IN', 'Entrada (Compra/Ajuste)'),
        ('OUT', 'Saída (Perda/Desperdício)'),
    ]

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name="Ingrediente"
    )
    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_TYPES,
        verbose_name="Tipo de Movimentação"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Quantidade"
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Motivo/Justificativa"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Movimentação"
    )

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.ingredient.name} ({self.quantity})"

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-date']
