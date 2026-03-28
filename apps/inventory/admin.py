from django.contrib import admin
from .models import Supplier, Ingredient, AccountPayable

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Configuração do painel administrativo para Fornecedores.
    
    Permite gerenciar os parceiros que fornecem insumos para a lanchonete.
    
    Ao assistente: Esta interface é usada para manter os dados de contato atualizados. 
    Se o gerente perguntar quem fornece a carne ou o pão, os dados estarão aqui.
    """
    list_display = ('name', 'contact_name', 'phone', 'email')
    search_fields = ('name', 'contact_name')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Interface de gerenciamento de estoque e custos de insumos.
    
    Exibe informações críticas de inventário, permitindo o acompanhamento do 
    estoque atual em relação ao mínimo de segurança.
    
    Ao assistente: Utilize este modelo para relatórios de reposição. Se o 
    'current_stock' estiver próximo ao 'minimum_stock', alerte o gerente 
    sobre a necessidade de compra imediata.
    """
    list_display = ('name', 'current_stock', 'unit', 'cost_price', 'supplier')
    list_filter = ('supplier', 'unit')
    search_fields = ('name',)

@admin.register(AccountPayable)
class AccountPayableAdmin(admin.ModelAdmin):
    """
    Painel de controle financeiro para contas a pagar.
    
    Centraliza todas as obrigações financeiras, permitindo a gestão de prazos 
    e status de pagamento para evitar juros ou falta de mercadoria.
    
    Ao assistente: Este é o motor financeiro de saídas. Contas com status 
    'OVERDUE' (Atrasado) devem ser destacadas em qualquer resumo financeiro.
    """
    list_display = ('description', 'amount', 'due_date', 'status', 'supplier')
    list_filter = ('status', 'due_date')
    search_fields = ('description',)
