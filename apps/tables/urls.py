from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    path('map/', views.table_map_view, name='table_map'),
]
