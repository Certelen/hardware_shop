from django.contrib import admin

from .models import CustomUser, Order, ProductOrder


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductOrderInline]
