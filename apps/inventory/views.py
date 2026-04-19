from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient, Category
from .forms import IngredientForm


def ingredient_list_view(request):
    ingredients_list = Ingredient.objects.all().select_related('supplier', 'category').order_by('name')
    categories = Category.objects.all()

    # Filtro por Nome
    search_query = request.GET.get('search')
    if search_query:
        ingredients_list = ingredients_list.filter(name__icontains=search_query)

    # Filtro por Categoria
    category_id = request.GET.get('category')
    if category_id:
        ingredients_list = ingredients_list.filter(category_id=category_id)

    # Paginação (10 itens por página)
    paginator = Paginator(ingredients_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'ingredients': page_obj,  # Agora passamos o objeto da página
        'categories': categories,
        'low_stock_count': Ingredient.objects.filter(current_stock__lte=F('minimum_stock')).count(),
    }
    return render(request, 'inventory/ingredient_list.html', context)


def ingredient_edit_view(request, pk=None):
    # Se houver PK, estamos editando. Se não, estamos criando (None).
    instance = get_object_or_404(Ingredient, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('inventory:ingredient_list')
    else:
        form = IngredientForm(instance=instance)
    
    return render(request, 'inventory/ingredient_form.html', {
        'form': form,
        'instance': instance
    })