import django.contrib.auth as auth
# import (
#     LoginView,
#     LogoutView,
#     PasswordChangeView,
#     PasswordResetView,
#     PasswordChangeDoneView,
#     PasswordResetDoneView,
#     PasswordResetConfirmView,
#     PasswordResetCompleteView
# )
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse

from .forms import CreationForm, UpdateUserForm
from .models import CustomUser
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
        return JsonResponse(status=200, data={'login': True})
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
        return JsonResponse(status=200, data={'login': True})
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
            return JsonResponse(status=200, data={'update': True})
        print(request.POST)
        context = {
            'profile_form': form
        }
        return render(request, 'user/profile.html', context)
    return reverse_lazy('products:index')


@login_required
def orders(request):
    pass


@login_required
def cart(request):
    user = request.user
    cart = user.order.filter(close=False)[0].product_order.all()
    final_amount = sum([obj.quantity for obj in cart])
    final_price = sum([obj.product.price*obj.quantity for obj in cart])
    if request.POST:
        raise ValueError(request.POST)
    context = {
        'cart': cart,
        'final_price': final_price,
        'final_amount': final_amount
    }
    return render(request, 'user/cart.html', context)


@login_required
def favorite(request, sort='popular'):
    user = request.user
    favorite_products = user.favorite_products.all()
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
        [favorite_products[i:i+3] for i in range(0, len(favorite_products), 3)]
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
