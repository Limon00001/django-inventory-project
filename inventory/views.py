from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from .admin import *
from .forms import *
from .models import StockHistory
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# Home Page
def home(request):
    title = 'Welcome to the Inventory Management System'
    context = {
        'title': title,
    }
    return render(request, 'home.html', context)


@login_required
# List of Items
def list_items(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        'title': title,
        'queryset': queryset,
        'form': form,
        'show_alerts': False,
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


@login_required
# Add Items
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item has been added successfully.')
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
            messages.success(request, 'Item has been updated successfully.')
            return redirect('/list_items')
    context = {
            'form': form,
            'title': 'Update Item'
        }
    return render(request, 'add_items.html', context)


# Delete Items
def delete_items(request, pk):
    queryset = Stock.objects.get(id = pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Item has been deleted successfully.')
        return redirect('/list_items')
    context = {
            'title': 'Delete Item',
            'header': 'Are you sure you want to delete?'
        }
    return render(request, 'delete_items.html', context)


# Stock Details Page
def stock_details(request,pk):
    queryset = Stock.objects.get(id = pk)
    context = {
        'queryset': queryset,
    }
    return render(request, 'stock_details.html', context)


# Issue Items
def issue_items(request, pk):
    queryset = Stock.objects.get(id = pk)
    form = IssueForm(request.POST or None, instance = queryset)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = instance.issue_to
        messages.success(request, "Issued Successfully! " + str(instance.quantity) + ' ' + str(instance.item_name) + 's now left in store')
        instance.save()
        return redirect('/stock_details/' + str(instance.id))
    
    context = {
        'title': 'Issue ' + str(queryset.item_name),
        'queryset': queryset,
        'form': form,
        'username': 'Issue By: ' + str(request.user),
    }
    return render(request, 'add_items.html', context)


# Receive Items
def receive_items(request, pk):
    queryset = Stock.objects.get(id = pk)
    form = ReceiveForm(request.POST or None, instance = queryset)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received Successfully! " + str(instance.quantity) + ' ' + str(instance.item_name) + 's now in store')
        return redirect('/stock_details/' + str(instance.id))
    
    context = {
        'title': 'Receive ' + str(queryset.item_name),
        'queryset': queryset,
        'form': form,
        'username': 'Received By: ' + str(request.user),
    }
    return render(request, 'add_items.html', context)


# Reorder Level
def reorder_level(request, pk):
    queryset = Stock.objects.get(id = pk)
    form = ReorderLevelForm(request.POST or None, instance = queryset)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, 'Reorder Level has been ' + str(instance.item_name) + ' is updated to ' + str(instance.reorder_level))

        return redirect('/list_items')
    context = {
            'instance': queryset,
            'form': form
        }
    return render(request, 'add_items.html', context)


# Sign up
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('login.html')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
        

# Sign In
def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('base.html')  # Change 'success_page_name' to the name of your success page
            else:
                # Invalid login credentials
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# Sign Out
def sign_out(request):
    logout(request)
    return redirect('login')


# Protected View
def my_protected_view(request):
    # Your view logic here
    return render(request, 'protected_view.html')


@login_required
# List History
def list_history(request):
    title = 'Items History'
    queryset = StockHistory.objects.all()
    form = StockSearchForm(request.POST or None)
    context = {
        'title': title,
        'queryset': queryset,
        'form': form,
        'show_alerts': False
    }
    if request.method == 'POST':
        category = form['category'].value
        # queryset = StockHistory.objects.filter(item_name__icontains = form['item_name'].value())
        queryset = Stock.objects.filter(category__icontains = form['category'].value(), item_name__icontains = form['item_name'].value())
        # if category != '':
        #     queryset = queryset.filter(category_id = category)

        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename = "Items History.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY', 'ISSUE QUANTITY', 'RECEIVE QUANTITY', 'RECEIVE BY', 'ISSUE BY', 'LAST UPDATED'])
            instance = queryset
            for items in instance:
                writer.writerow([items.category, items.item_name, items.quantity, items.issue_quantity, items.receive_quantity, items.receive_by, items.issue_by, items.last_updated])
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
    return render(request, 'list_history.html', context)