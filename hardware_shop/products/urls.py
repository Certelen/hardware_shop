from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path(
        '', views.index, name='index'
    ),
    path(
        'search', views.search, name='search'
    ),
    path(
        'change_cart', views.change_cart, name='change_cart'
    ),
    path(
        'change_favorite', views.change_favorite, name='change_favorite'
    ),
    path(
        'category/<int:category_id>/', views.category, name='category'
    ),
    path(
        'product/<int:product_id>/', views.product_detail, name='product'
    ),

]
