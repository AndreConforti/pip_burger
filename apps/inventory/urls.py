from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('ingredients/', views.ingredient_list_view, name='ingredient_list'),
    path('ingredients/add/', views.ingredient_edit_view, name='ingredient_add'),
    path('ingredients/<int:pk>/edit/', views.ingredient_edit_view, name='ingredient_edit'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('movement/add/', views.StockMovementCreateView.as_view(), name='stock_movement_add'),
    path('movements/', views.StockMovementListView.as_view(), name='stock_movement_list'),
]
