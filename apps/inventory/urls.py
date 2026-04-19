from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('ingredients/', views.ingredient_list_view, name='ingredient_list'),
    path('ingredients/add/', views.ingredient_edit_view, name='ingredient_add'),
    path('ingredients/<int:pk>/edit/', views.ingredient_edit_view, name='ingredient_edit'),
]
