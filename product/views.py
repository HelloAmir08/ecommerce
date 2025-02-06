from django.shortcuts import render, get_object_or_404, redirect

from product.models import Product, Category, Comment
from product.forms import CommentForm

def product_list(request):
    search_query = request.GET.get('q', '')
    categories=Category.objects.all()
    sort_option = request.GET.get('sort', 'rating')
    if sort_option == 'newest':
        products = Product.objects.order_by('-id')
    elif sort_option == 'price':
        products = Product.objects.order_by('-price')
    else:
        products = Product.objects.order_by('-rating')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    context={
        'products':products,
        'categories':categories,
        'sort_option':sort_option,
    }
    return render(request, "product/product-list.html", context=context)




def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=pk)
    context = {
        'product': product,
        'comments': comments,
    }
    return render(request, 'product/product-details.html', context=context)




def comment_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('comment_detail', pk=product.pk)
    else:
        form = CommentForm()
    context={
        'product': product,
        'form': form,
        'comments': Comment.objects.filter(product=pk),
    }

    comments = Comment.objects.filter(product=product)
    return render(request, 'product/product-details.html', context=context)

