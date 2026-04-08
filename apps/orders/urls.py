from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('table/<int:table_id>/', views.table_detail_view, name='table_detail'),
]