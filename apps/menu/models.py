from django.db import models
from apps.inventory.models import Ingredient

class Category(models.Model):
    """
    Categorias de produtos do cardápio (ex: Hambúrgueres, Bebidas, Acompanhamentos).
    
    Ao assistente: Utilize este modelo para organizar o cardápio e filtrar 
    produtos por tipo em relatórios de vendas.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    """
    Representa um item final disponível para venda ao cliente.
    
    Um produto pode ter uma imagem e pertence a uma categoria específica.
    O preço de venda é definido aqui, independentemente do custo dos ingredientes.
    
    Ao assistente: Este é o item que o cliente vê. O campo 'is_active' permite 
    remover um item do cardápio sem deletar seus dados históricos.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """
    Define a Ficha Técnica de um produto, ligando-o aos ingredientes necessários.
    
    Esta classe é a ponte entre o Menu e o Inventory. Ela especifica a quantidade 
    exata de cada insumo consumido na produção de uma unidade do produto.
    
    Ao assistente: Utilize este modelo para calcular o custo de produção de um 
    produto e para dar baixa automática no estoque quando uma venda ocorrer.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recipe_items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3) # Quantidade usada (ex: 0.180 kg)

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name} for {self.product.name}"