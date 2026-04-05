from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    """
    Itens consumidos no pedido.
    """
    model = OrderItem
    extra = 1
    autocomplete_fields = ['product']

class PaymentInline(admin.TabularInline):
    """
    Pagamentos realizados para este pedido.
    """
    model = Payment
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Painel de controle da comanda.
    """
    list_display = ('id', 'table', 'customer_name', 'status', 'total_value', 'total_paid', 'balance_due')
    list_filter = ('status', 'table')
    search_fields = ('customer_name', 'table__number')
    list_editable = ('status',)
    
    # Agora temos dois inlines: Itens e Pagamentos
    inlines = [OrderItemInline, PaymentInline]
    
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)