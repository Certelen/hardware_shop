from django.contrib import admin

from .models import Category, Product, ProductImage, ProductChar, CategoryChar


class CategoryCharInline(admin.TabularInline):
    model = CategoryChar
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryCharInline,]


class ProductCharInline(admin.TabularInline):
    model = ProductChar
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductCharInline, ProductImageInline]

    class Media:
        js = ['js/category_admin.js',
              'js/jquery.min.js']
