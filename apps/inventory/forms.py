from django import forms
from .models import Ingredient, StockMovement   


class IngredientForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de dados cadastrais dos ingredientes.
    
    O campo 'current_stock' foi removido intencionalmente deste formulário 
    para garantir que alterações no saldo físico do estoque sejam realizadas 
    exclusivamente através do módulo de movimentações, mantendo o histórico confiável.
    """
    class Meta:
        model = Ingredient
        # Removemos 'current_stock' desta lista
        fields = ['name', 'category', 'supplier', 'unit', 'minimum_stock', 'cost_price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do Insumo'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-select',
            }),
            'unit': forms.Select(attrs={
                'class': 'form-select',
            }),
            'minimum_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }


class StockMovementForm(forms.ModelForm):
    """
    Formulário para registro de movimentações de estoque (entradas e saídas).
    
    Este formulário expõe os campos necessários para que o operador informe
    qual ingrediente está sendo movimentado, o tipo de operação, a quantidade
    e uma justificativa para fins de auditoria do inventário.
    """
    class Meta:
        model = StockMovement
        fields = ['ingredient', 'movement_type', 'quantity', 'reason']
        widgets = {
            'ingredient': forms.Select(attrs={
                'class': 'form-select'
            }),
            'movement_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'reason': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Compra semanal, Item vencido, etc.'
            }),
        }

    def clean_quantity(self):
        """
        Garante que a quantidade informada seja sempre maior que zero.
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantity