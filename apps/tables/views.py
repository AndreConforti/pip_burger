from django.shortcuts import render
from .models import Table

def table_map_view(request):
    """
    Busca todas as mesas e renderiza o mapa visual para o usuário.
    """
    tables = Table.objects.all()
    context = {
        'tables': tables
    }
    return render(request, 'tables/table_map.html', context)