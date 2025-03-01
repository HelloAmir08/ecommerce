from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from product.models import Product, Category, Comment
from product.forms import CommentForm
from customer.models import Customer


def product_list(request):
    customers = Customer.objects.all()
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()
    sort_option = request.GET.get('sort', 'rating')

    if sort_option == 'newest':
        products = Product.objects.order_by('-id')
    elif sort_option == 'price':
        products = Product.objects.order_by('-price')
    else:
        products = Product.objects.order_by('-rating')

    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'customers': customers,
        'products': page_obj,
        'categories': categories,
        'sort_option': sort_option,
        'page_obj': page_obj,
        'user': request.user,
    }
    return render(request, "product/product-list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = Comment.objects.filter(product=product)
    context = {
        'product': product,
        'comments': comments,
        'user': request.user,
    }
    return render(request, 'product/product-details.html', context=context)


def comment_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('comment_detail', slug=product.slug)
    else:
        form = CommentForm()

    context = {
        'product': product,
        'form': form,
        'comments': Comment.objects.filter(product=product),
    }
    return render(request, 'product/product-details.html', context=context)
