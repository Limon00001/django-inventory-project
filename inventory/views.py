from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from .admin import *
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm
from django.contrib import messages

# Create your views here.

# Home Page
def home(request):
    title = 'Welcome to the Inventory Management System'
    context = {
        'title': title,
    }
    return render(request, 'home.html', context)


# List of Items
def list_items(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        'title': title,
        'queryset': queryset,
        'form': form,
        'show_alerts': False
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains = form['category'].value(), item_name__icontains = form['item_name'].value())
        
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename = "Items List.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for items in instance:
                writer.writerow([items.category, items.item_name, items.quantity])
            return response
        
        context = {
            'form': form,
            'title': title,
            'queryset': queryset
        }
        if not queryset.exists():
            context['show_alert'] = True,
            messages.warning(request, 'No items found matching the search criteria.')
        else:
            context['queryset'] = queryset
    return render(request, 'list_items.html', context)


# Add Items
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/list_items')
    context = {
        'form': form,
        'title': 'Add Item',
    }
    return render(request, 'add_items.html', context)


# Update Items
def update_items(request, pk):
    queryset = Stock.objects.get(id = pk)
    form = StockUpdateForm(instance = queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance = queryset)
        if form.is_valid():
            form.save()
            return redirect('/list_items')
    context = {
            'form': form,
        }
    return render(request, 'add_items.html', context)


# Delete Items
def delete_items(request, pk):
    queryset = Stock.objects.get(id = pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/list_items')
    context = {
            'title': 'Delete Item',
            'header': 'Are you sure you want to delete?'
        }
    return render(request, 'delete_items.html', context)