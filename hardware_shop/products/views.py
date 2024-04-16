from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


from users.models import ProductOrder
from .models import Category, Product
from .forms import SearchForm


def index(request, now_order=None):
    form = SearchForm()
    if request.user.is_authenticated:
        now_order = request.user.order.filter(close=False)[0]
        now_order = now_order.product_order.all()
        now_order = now_order.values_list('product', flat=True)
        favorite_products = request.user.favorite_products.all()
        favorite_products = favorite_products.values_list(flat=True)
    context = {
        'search_form': form,
        'now_order': now_order,
        'favorite_products': favorite_products,
        'categorys': Category.objects.all(),
        'popular': Product.objects.all()[:5]
    }
    return render(request, 'index/index.html', context)


def search(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            form_input = form_input.get('search_product')
            search_return = Product.objects.filter(
                Q(name__contains=form_input))
    context = {
        'categorys': Category.objects.all(),
        'products': search_return
    }
    raise ValueError(context)


def product_detail(request, product_id):
    pass


@login_required
def change_cart(request):
    if request.method == "POST":
        product = Product.objects.get(id=request.POST['product'])
        order = request.user.order.filter(
            close=False)[0]
        product_order = order.product_order.filter(product=product)
        if product_order:
            product_order[0].delete()
        else:
            ProductOrder.objects.create(
                order=order, product=product, quantity=1)
        now_order = order.product_order.all()
        now_order = now_order.values_list('product', flat=True)
        context = {
            'product': product,
            'now_order': now_order
        }
        return render(request, 'products/in-out_cart.html', context)
    return reverse_lazy('products:index')


@login_required
def change_favorite(request):
    if request.method == "POST":
        user = request.user
        product = Product.objects.get(id=request.POST['product'])
        favorite_products = user.favorite_products.all()
        favorite_product = favorite_products.filter(id=product.id)
        if favorite_product:
            user.favorite_products.remove(product)
        else:
            user.favorite_products.add(product)
        favorite_products = favorite_products.values_list(flat=True)
        context = {
            'product': product,
            'favorite_products': favorite_products
        }
        return render(request, 'products/in-out_favorite.html', context)
    return reverse_lazy('products:index')


def category(request, category_name):
    pass


def above(request):
    pass
