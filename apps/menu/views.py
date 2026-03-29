from django.shortcuts import render

def test_view(request):
    """View temporária para testar o Bootstrap e o CSS do André"""
    return render(request, 'test_dashboard.html')
