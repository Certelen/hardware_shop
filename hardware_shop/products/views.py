from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from http import HTTPStatus


from users.models import ProductOrder, Review
from .models import Category, Product
from .forms import SearchForm
from hardware_shop.settings import MAX_ROW_ON_PAGE


def paginator(request, products, page_number=False):
    paginator = Paginator(products, MAX_ROW_ON_PAGE)
    if not page_number:
        page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def context_forms(request, now_order=None):
    form = SearchForm()
    context_auth = {}
    if request.user.is_authenticated:
        now_order = request.user.order.filter(close='0')[0]
        now_order = now_order.product_order.all()
        now_order = now_order.values_list('product', flat=True)
        favorite_products = request.user.favorite_products.all()
        favorite_products = favorite_products.values_list(flat=True)
        context_auth = {
            'now_order': now_order,
            'favorite_products': favorite_products
        }
    context = {
        'search_form': form,
        'categorys': Category.objects.all()
    }
    context = dict(
        list(context.items()) +
        list(context_auth.items())
    )
    return context


def index(request):
    context = {
        'popular': Product.objects.all().order_by('-score')[:5]
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
    return render(request, 'index/index.html', context)


def search(request, sort='popular', select_page=1, search_word=''):
    search_return = Product.objects.none()
    form = SearchForm()
    context = {}
    if request.method == 'POST':
        data = request.POST
        sort = data.get('sort_type', sort)
        select_page = data.get('select_page', select_page)
        form = SearchForm(data=data)
        if form.is_valid():
            search_word = form.cleaned_data.get('search_product')
        search_return = Product.objects.filter(
            Q(name__iregex=search_word))
    if sort == 'popular':
        search_return = search_return.order_by('score')
    elif sort == 'alphabet':
        search_return = search_return.order_by('name')
    elif sort == 'min_price':
        search_return = search_return.order_by('price')
    elif sort == 'max_price':
        search_return = search_return.order_by('price').reverse()
    page_obj = paginator(
        request,
        search_return,
        select_page
    )
    context = {
        'products': search_return,
        'page_obj': page_obj,
        'search_word': search_word,
        'now_sort': sort,
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
    return render(request, 'products/search.html', context)


def product_detail(request, product_id, quantity=1):
    product = get_object_or_404(Product, id=product_id)
    images = [product.main_image]
    images += [obj.image for obj in product.images.all()]
    if request.user.is_authenticated:
        order = request.user.order.filter(close='0')
        if order:
            product_order = ProductOrder.objects.filter(
                order=order[0], product=product)
            if product_order:
                quantity = product_order[0].quantity
    comments = Review.objects.filter(product=product)
    context = {
        'product': product,
        'images': images,
        'quantity': quantity,
        'comments': comments,
        'chars': product.char.all()
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
    return render(request, 'products/product-detail.html', context)


@login_required
def change_cart(request):
    if request.method == "POST":
        product = Product.objects.get(id=request.POST['product'])
        if product.quantity < 0:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'reload': ''}
            )
        order = request.user.order.filter(
            close='0')[0]
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


def get_category_char(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category_char = category.char.values_list('characteristic_name', flat=True)
    return JsonResponse(
        status=HTTPStatus.OK,
        data={'char': list(category_char)}
    )


def category(request, category_id, sort='popular', select_page=1):
    category = get_object_or_404(Category, id=category_id)
    products = category.product.all()
    filter_status = {}
    filters = {}
    for char in category.char.all():
        char = char.characteristic_name
        for product in products:
            product_char = product.char.filter(characteristic_name=char)
            for char_value in product_char:
                if char in filters:
                    filters[char][char_value.characteristic_value] = False
                else:
                    filters[char] = {char_value.characteristic_value: False}
    if request.method == "POST":
        data = request.POST
        if 'apply' in data:
            min_price = data['min_price']
            max_price = data['max_price']
            sort = data['sort_type']
            filters_data = data.getlist('filters')
            select_page = int(data['select_page'])
            if min_price or max_price:
                if not min_price:
                    min_price = 0
                elif not max_price:
                    min_price = 9999999
                min_price = int(min_price)
                max_price = int(max_price)
                if min_price > max_price:
                    max_price = min_price + 1
                products = products.filter(
                    price__range=(min_price, max_price)
                )
                filter_status = {
                    'min_price': min_price,
                    'max_price': max_price,
                }
            if filters_data:
                for filter_value in filters_data:
                    char_name, char_value = filter_value.split('; ')
                    products = products.filter(
                        char__characteristic_name=char_name
                    )
                    products = products.filter(
                        char__characteristic_value=char_value
                    )
                    print(products)
                    filters[char_name][char_value] = True

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
        products,
        select_page
    )
    context = {
        'now_sort': sort,
        'page_obj': page_obj,
        'category': category,
        'filters': filters
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items()) +
        list(filter_status.items())
    )
    return render(request, 'products/category.html', context)


def page_not_found(request, exception):
    return render(
        request, 'auth/404.html',
        status=HTTPStatus.NOT_FOUND
    )
