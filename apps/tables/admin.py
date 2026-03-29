from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'capacity', 'current_customers', 'linked_to')
    list_editable = ('status', 'current_customers') # Permite mudar o status direto na lista!
    list_filter = ('status',)