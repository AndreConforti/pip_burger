from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Ingredient, Category
from .forms import IngredientForm


def ingredient_list_view(request):
    """
    Exibe a lista de ingredientes com suporte a filtros, 
    paginação e busca global para autocomplete.
    """
    ingredients_list = Ingredient.objects.all().select_related('supplier', 'category').order_by('name')
    categories = Category.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        ingredients_list = ingredients_list.filter(name__icontains=search_query)

    category_id = request.GET.get('category')
    if category_id:
        ingredients_list = ingredients_list.filter(category_id=category_id)

    paginator = Paginator(ingredients_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'ingredients': page_obj,
        'categories': categories,
        'low_stock_count': Ingredient.objects.filter(current_stock__lte=F('minimum_stock')).count(),
        'all_ingredient_names': Ingredient.objects.values_list('name', flat=True),
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

class CategoryListView(ListView):
    """Lista todas as categorias cadastradas"""
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    """Cria uma nova categoria"""
    model = Category
    fields = ['name']
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('inventory:category_list')

class CategoryUpdateView(UpdateView):
    """Edita uma categoria existente"""
    model = Category
    fields = ['name']
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('inventory:category_list')

class CategoryDeleteView(DeleteView):
    """Exclui uma categoria via POST (acionada pelo Modal)"""
    model = Category
    success_url = reverse_lazy('inventory:category_list')

    # Adicione este método para evitar que o Django procure o template .html
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)