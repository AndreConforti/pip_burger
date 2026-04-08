from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    path('map/', views.table_map_view, name='table_map'),
    path('<int:table_id>/', views.table_detail_view, name='table_detail'),
    path('<int:table_id>/join/', views.join_table_action, name='join_table_action'),
    path('<int:table_id>/occupy/', views.occupy_table_action, name='occupy_table_action'),
]
