from django.shortcuts import render, get_object_or_404, redirect

from customer.models import Customer
from customer.forms import CustomerForm


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
