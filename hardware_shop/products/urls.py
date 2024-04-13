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
        'category/<str:category_name>/', views.category, name='category'
    ),
]
