from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path(
        'profile', views.profile, name='profile'
    ),
    path(
        'orders', views.orders, name='orders'
    ),
    path(
        'cart', views.cart, name='cart'
    ),
    path(
        'favorite', views.favorite, name='favorite'
    ),
]
