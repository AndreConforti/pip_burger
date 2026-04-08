from django.shortcuts import render, get_object_or_404
from apps.tables.models import Table
from .models import Order

def table_detail_view(request, table_id):
    """
    Exibe os detalhes de uma mesa específica e suas comandas ativas.
    
    Esta view busca a mesa pelo ID e filtra apenas as ordens com status 
    'open' ou 'closing'. Se a mesa estiver unida a outra (linked_to), 
    o sistema deve focar na mesa mestra para lançamentos financeiros.
    Utilizada para renderizar a página de consumo e gestão da mesa.
    """
    # Busca a mesa ou retorna 404
    table = get_object_or_404(Table, id=table_id)
    
    # Filtra pedidos ativos (exclui pagos e cancelados)
    active_orders = table.orders.filter(status__in=['open', 'closing'])
    
    context = {
        'table': table,
        'active_orders': active_orders,
    }
    
    return render(request, 'orders/table_detail.html', context)