import django.contrib.auth as auth
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from datetime import date
from http import HTTPStatus

from .forms import CreationForm, UpdateUserForm
from .models import CustomUser, Order, Review
from products.models import Product
from products.views import paginator, context_forms


def signup(request):
    if request.method == "POST":
        form = CreationForm(data=request.POST)
        if not form.is_valid():
            context = {
                'signup_form': form
            }
            return render(request, 'auth/signup.html', context)
        new_user = form.save()
        auth.login(request, new_user)
        return JsonResponse(status=HTTPStatus.OK, data={'login': True})
    return reverse_lazy('products:index')


def login(request):
    if request.method == "POST":
        form = auth.forms.AuthenticationForm(data=request.POST)
        if not form.is_valid():
            context = {
                'login_form': form
            }
            return render(request, 'auth/login.html', context)
        auth.login(request, form.get_user())
        return JsonResponse(status=HTTPStatus.OK, data={'login': True})
    return reverse_lazy('products:index')


@login_required
def profile(request):
    if request.method == "POST":
        form = UpdateUserForm(
            request.POST, instance=CustomUser.objects.get(id=request.user.id))
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            if (request.POST['password1'] and
                    request.POST['password1'] == request.POST['password2']):
                new_password = request.POST['password1']
                user = CustomUser.objects.get(email=request.user.email)
                user.set_password(new_password)
                user.save()
            return JsonResponse(status=HTTPStatus.OK, data={'update': True})
        context = {
            'profile_form': form
        }
        return render(request, 'user/profile.html', context)
    return reverse_lazy('products:index')


@login_required
def orders(request):
    user = request.user
    orders = user.order.filter(~Q(close='0'))
    product_order = [order.product_order.all() for order in orders]
    page_obj = paginator(
        request,
        [product_order[i:i+1] for i in range(0, len(product_order))]
    )
    context = {
        'page_obj': page_obj
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
    return render(request, 'user/orders.html', context)


@login_required
def cart(request):
    user = request.user
    user_order = user.order.filter(close='0')[0]
    cart = user_order.product_order.all()
    final_amount = sum([obj.quantity for obj in cart])
    final_price = sum([obj.product.price*obj.quantity for obj in cart])
    if request.POST:
        if not request.POST['quantity'] or not request.POST['product']:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Добавьте товары в заказ'})
        quantity_list = list(map(int, request.POST['quantity'].split(',')))
        product_list = list(map(int, request.POST['product'].split(',')))
        if 'phone' not in request.POST:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Укажите номер телефона'})
        phone = request.POST['phone']
        if 'address' not in request.POST:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Укажите номер адрес'})
        address = request.POST['address']
        changed_list = []
        for index in range(len(product_list)):
            order_obj = cart.filter(product=product_list[index])
            if not order_obj:
                return JsonResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    data={'error': 'В вашей корзине нет одного из товаров'})
            order_obj = order_obj[0]
            if order_obj.product.quantity < quantity_list[index]:
                return JsonResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    data={
                        'error': f'Товара {order_obj.product.name} осталось\
                            {order_obj.product.quantity} шт.'})
            order_obj.quantity = quantity_list[index]
            product = order_obj.product
            product.quantity -= quantity_list[index]
            changed_list.append(order_obj)
            changed_list.append(product)
        for obj in changed_list:
            obj.save()
        if not user.phone:
            user.phone = phone
            user.save()
        user_order.number = user.phone
        user_order.address = address
        user_order.close = 1
        user_order.close_data = date.today()
        user_order.save()
        Order.objects.create(user=user)
        return JsonResponse(status=HTTPStatus.OK, data={})

    context = {
        'cart': cart,
        'final_price': final_price,
        'final_amount': final_amount
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
    return render(request, 'user/cart.html', context)


@login_required
def favorite(request, sort='popular', select_page=1):
    user = request.user
    favorite_products = user.favorite_products.all()
    if request.method == 'POST':
        data = request.POST
        sort = data.get('sort_type', sort)
        select_page = data.get('select_page', select_page)
    if sort == 'popular':
        favorite_products = favorite_products.order_by('score')
    elif sort == 'alphabet':
        favorite_products = favorite_products.order_by('name')
    elif sort == 'min_price':
        favorite_products = favorite_products.order_by('price')
    elif sort == 'max_price':
        favorite_products = favorite_products.order_by('price').reverse()
    page_obj = paginator(
        request,
        favorite_products,
        select_page
    )
    context = {
        'now_sort': sort,
        'page_obj': page_obj
    }
    context = dict(
        list(context.items()) +
        list(context_forms(request).items())
    )
    return render(request, 'user/favorite.html', context)


@login_required
def review(request, product_id):
    if request.method == 'POST':
        data = request.POST
        if not data['text']:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Укажите текст комментария'})
        if len(data['text']) < 80:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Текст комментария должен\
                    содержать не менее 80 символов'})
        if not data['title']:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Укажите заголовок комментария'})
        if len(data['title']) < 10:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Заголовок комментария должен\
                    содержать не менее 10 символов'})
        if not data['score']:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Укажите оценку к товару'})
        if 0 >= int(data['score']) > 5:
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Укажите оценку к товару от 1 до 5'})
        if not Product.objects.filter(id=product_id):
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={'error': 'Неверный товар'})
        product = Product.objects.get(id=product_id)
        Review.objects.create(
            user=request.user,
            product=product,
            title=data['title'],
            comment=data['text'],
            score=data['score']
        )
        score_list = [review.score for review in product.review.all()]
        product.score = sum(score_list) / len(score_list)
        product.save()
        return JsonResponse(status=HTTPStatus.OK, data={})
    return reverse_lazy('products:index')


@login_required
def delete_review(request, product_id, comment_id):
    comment = get_object_or_404(Review, id=comment_id)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST' and request.user == comment.user:
        comment.delete()
        score_list = [review.score for review in product.review.all()]
        product.score = sum(score_list) / len(score_list)
        product.save()
        return redirect('products:product', product_id=product_id)
    return redirect('products:product product_id', product_id=product_id)
