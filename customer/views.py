from django.shortcuts import render, get_object_or_404, redirect
import openpyxl
from django.http import HttpResponse
from customer.models import Customer
from customer.forms import CustomerForm
from django.http import JsonResponse
import json



def customer_page(request):
    search_query = request.GET.get('q', '')
    customers = Customer.objects.all()
    if search_query:
        customers = Customer.objects.filter(full_name__icontains=search_query)
    context = {
        'customers': customers
    }
    return render(request, 'customer/customers.html', context=context )

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    return render(request, "customer/customer-details.html", {'customer': customer})


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customer_page')
    else:
        form = CustomerForm()

    return render(request, 'customer/customer_create.html', {'form': form})

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_page')
    else:
        form = CustomerForm(instance=customer)

    context = {'form': form, 'customer': customer}
    return render(request, 'customer/customer_create.html', context)

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    customer.delete()
    return redirect('customer_page')


def export_customers_json(request):
    customers = Customer.objects.all()

    data = []
    for customer in customers:
        data.append({
            'id': customer.id,
            'full_name': customer.full_name,
            'email': customer.email,
            'phone': str(customer.phone),
            'address': customer.address,
            'image': request.build_absolute_uri(customer.get_absolute_url)
        })

    response = HttpResponse(json.dumps(data, indent=4), content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename="customers.json"'
    return response

def export_customers_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Customers"
    headers = ['ID', 'Full Name', 'Email', 'Phone', 'Address', 'Image URL']
    sheet.append(headers)
    customers = Customer.objects.all()
    for customer in customers:
        sheet.append([
            customer.id,
            customer.full_name,
            customer.email,
            str(customer.phone),
            customer.address,
            request.build_absolute_uri(customer.get_absolute_url)
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'

    workbook.save(response)

    return response
