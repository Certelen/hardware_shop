from django.shortcuts import render

from .models import Category, Product


def index(request):
    context = {
        'categorys': Category.objects.all(),
        'popular': Product.objects.all()[:5]
    }
    return render(request, 'index/index.html', context)


def search(request):
    pass


def category(request, category_name):
    pass


def above(request):
    pass
