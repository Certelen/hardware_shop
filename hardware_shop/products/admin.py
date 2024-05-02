from django.contrib import admin

from .models import Category, Product, ProductImage, ProductChar


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductCharInline(admin.TabularInline):
    model = ProductChar
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductCharInline, ProductImageInline]
