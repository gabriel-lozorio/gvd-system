from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from .models import Category
from .forms import CategoryForm

@login_required
def category_list(request):
    """
    Lista de categorias
    """
    categories = Category.objects.all().order_by('name')
    return render(request, 'categories/list.html', {'categories': categories})

@login_required
def category_create(request):
    """
    Criação de categoria
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Categoria criada com sucesso!"))
            return redirect('category-list')
    else:
        form = CategoryForm()
    
    return render(request, 'categories/form.html', {
        'form': form,
        'is_creating': True
    })

@login_required
def category_detail(request, pk):
    """
    Detalhes da categoria
    """
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'categories/detail.html', {'category': category})

@login_required
def category_update(request, pk):
    """
    Atualização de categoria
    """
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _("Categoria atualizada com sucesso!"))
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'categories/form.html', {
        'form': form,
        'category': category,
        'is_creating': False
    })