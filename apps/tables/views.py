from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Table
from apps.orders.models import Order


def table_map_view(request):
    """
    Busca todas as mesas e renderiza o mapa visual para o usuário.
    """
    tables = Table.objects.all()
    context = {
        'tables': tables
    }
    return render(request, 'tables/table_map.html', context)


def join_tables_view(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    
    if request.method == 'POST':
        master_table_id = request.POST.get('master_table')
        master_table = get_object_or_404(Table, id=master_table_id)
        
        try:
            table.join_with(master_table)
            messages.success(request, f"Mesa {table.number} unida à Mesa {master_table.number}!")
        except Exception as e:
            messages.error(request, "Erro ao unir mesas.")
            
    return redirect('tables:table_detail', table_id=table.id)


def join_table_action(request, table_id):
    """Processa a união ou desunião de mesas."""
    if request.method == "POST":
        current_table = get_object_or_404(Table, id=table_id)
        master_table_id = request.POST.get("master_table_id")
        
        if master_table_id:
            master_table = get_object_or_404(Table, id=master_table_id)
            current_table.linked_to = master_table
            current_table.status = 'occupied'
            current_table.save()
            messages.success(request, f"Mesa {current_table.number} unida à Mesa {master_table.number}!")
        else:
            current_table.linked_to = None
            
            # Verifica se existem comandas abertas antes de liberar a mesa
            has_active_orders = current_table.orders.filter(status__in=['open', 'closing']).exists()
            
            if has_active_orders:
                current_table.status = 'occupied'
            else:
                current_table.status = 'available'
                
            current_table.save()
            messages.info(request, f"Mesa {current_table.number} agora está individual.")
            
    return redirect('tables:table_detail', table_id=table_id)


def table_detail_view(request, table_id):
    """Exibe os detalhes de uma mesa específica e suas comandas ativas."""
    table = get_object_or_404(Table, id=table_id)
    
    # Filtra pedidos ativos (exclui pagos e cancelados)
    active_orders = table.orders.filter(status__in=['open', 'closing'])
    
    # Busca todas as mesas exceto a atual (para o Modal de União)
    all_tables = Table.objects.exclude(id=table.id).order_by('number')
    
    context = {
        'table': table,
        'active_orders': active_orders,
        'all_tables': all_tables,
    }
    return render(request, 'tables/table_detail.html', context)


def occupy_table_action(request, table_id):
    """
    Altera o status da mesa para ocupada manualmente, 
    mesmo antes de existir uma comanda vinculada.
    """
    table = get_object_or_404(Table, id=table_id)
    table = get_object_or_404(Table, id=table_id)
    if table.status == 'available':
        table.status = 'occupied'
        table.save()
        messages.success(request, f"Mesa {table.number} ocupada!")
    return redirect('tables:table_detail', table_id=table.id)