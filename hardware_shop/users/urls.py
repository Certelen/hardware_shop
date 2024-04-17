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
        'favorite/<str:sort>', views.favorite, name='sort'
    ),
    path(
        'favorite/', views.favorite, name='favorite'
    ),
    path(
        'review/<int:product_id>/', views.review, name='review'
    ),
]

"""Авторизация"""
urlpatterns += [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
