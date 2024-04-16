from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse


from users.models import ProductOrder
from .models import Category, Product
from .forms import SearchForm
from hardware_shop.settings import MAX_ROW_ON_PAGE


def paginator(request, row_list):
    paginator = Paginator(row_list, MAX_ROW_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def context_forms(request, now_order=None):
    form = SearchForm()
    if request.user.is_authenticated:
        now_order = request.user.order.filter(close=False)[0]
        now_order = now_order.product_order.all()
        now_order = now_order.values_list('product', flat=True)
        favorite_products = request.user.favorite_products.all()
        favorite_products = favorite_products.values_list(flat=True)
    return {
        'search_form': form,
        'now_order': now_order,
        'favorite_products': favorite_products,
        'categorys': Category.objects.all()
    }


def index(request, now_order=None):
    context = {
        'categorys': Category.objects.all(),
        'popular': Product.objects.all()[:5]
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
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


def product_detail(request, product_id, quantity=1):
    product = get_object_or_404(Product, id=product_id)
    images = [product.main_image]
    images += [obj.image for obj in product.images.all()]
    order = request.user.order.filter(close=False)
    if order:
        product_order = ProductOrder.objects.filter(
            order=order[0], product=product)
        if product_order:
            quantity = product_order[0].quantity
    context = {
        'product': product,
        'images': images,
        'quantity': quantity
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
    return render(request, 'products/product-detail.html', context)


@login_required
def change_cart(request):
    if request.method == "POST":
        print(request.POST)
        product = Product.objects.get(id=request.POST['product'])
        if product.quantity < 0:
            return JsonResponse(status=400, data={'reload': ''})
        order = request.user.order.filter(
            close=False)[0]
        product_order = order.product_order.filter(product=product)
        if 'quantity' in request.POST and request.POST['quantity']:
            quantity = int(request.POST['quantity'])
        else:
            quantity = 1
        if product_order:
            if 'delete' in request.POST:
                product_order[0].delete()
            elif product_order[0].quantity == quantity:
                product_order[0].delete()
            else:
                product_order[0].quantity = quantity
                product_order[0].save()
        else:
            ProductOrder.objects.create(
                order=order, product=product, quantity=quantity)
        now_order = order.product_order.all()
        now_order = now_order.values_list('product', flat=True)
        context = {
            'product': product,
            'now_order': now_order,
            'quantity': quantity
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


def category(request, category_id, sort='popular', filter_str='-'):
    category = get_object_or_404(Category, id=category_id)
    products = category.product.all()
    filter_status = {}
    if filter_str != '-':
        filter_str = list(map(int, filter_str.split('-')))
        if filter_str[0] > filter_str[1]:
            filter_str[1] = filter_str[0] + 1
        products = products.filter(
            price__range=(filter_str[0], filter_str[1]))
        filter_status = {
            'filter': True,
            'min_price': filter_str[0],
            'max_price': filter_str[1],
            'filter_link': f'{str(filter_str[0])}-{str(filter_str[1])}'
        }
    if request.method == "POST":
        data = request.POST
        if 'apply' in data:
            min_price = int(data['min_price'])
            max_price = int(data['max_price'])
            if min_price > max_price:
                max_price = min_price + 1
            products = products.filter(
                price__range=(min_price, max_price)
            )
            filter_status = {
                'filter': True,
                'min_price': min_price,
                'max_price': max_price,
                'filter_link': f'{str(min_price)}-{str(max_price)}'
            }
        elif 'reset' in data:
            filter_status = {'filter': False}
    if sort == 'popular':
        products = products.order_by('score')
    elif sort == 'alphabet':
        products = products.order_by('name')
    elif sort == 'min_price':
        products = products.order_by('price')
    elif sort == 'max_price':
        products = products.order_by('price').reverse()
    page_obj = paginator(
        request,
        [products[i:i+3] for i in range(0, len(products), 3)]
    )
    context = {
        'now_sort': sort,
        'page_obj': page_obj,
        'category': category
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items()) +
        list(filter_status.items())
    )
    return render(request, 'products/category.html', context)


def above(request):
    pass
