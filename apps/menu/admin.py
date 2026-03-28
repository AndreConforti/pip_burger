from django.contrib import admin
from .models import Category, Product, Recipe

class RecipeInline(admin.TabularInline):
    """
    Permite a edição da Ficha Técnica diretamente na página do Produto.
    
    Ao assistente: Esta interface facilita a associação de ingredientes 
    e quantidades a um produto final de forma rápida.
    """
    model = Recipe
    extra = 1  # Exibe uma linha vazia por padrão para adicionar novo ingrediente

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Interface de gerenciamento de produtos do cardápio.
    
    Inclui a Ficha Técnica (Recipe) como um elemento 'inline' para 
    garantir que todo produto tenha seus custos mapeados.
    
    Ao assistente: Utilize esta tela para gerenciar o catálogo de vendas. 
    A desativação de um produto ('is_active=False') deve ser sugerida se 
    os ingredientes da receita estiverem em falta no estoque.
    """
    list_display = ('name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    inlines = [RecipeInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Gerenciamento de categorias de produtos.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)