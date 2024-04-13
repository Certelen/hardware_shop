from django.db import models
from django.contrib.auth.models import AbstractUser

from products.models import Product


class CustomUser(AbstractUser):
    favorite_products = models.ManyToManyField(
        Product,
        related_name='users',
        verbose_name='Избранные товары',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name='Заказ пользователя',
    )
    number = models.CharField(
        'Номер получателя',
        help_text='Номер получателя',
        max_length=11,
    )
    adress = models.CharField(
        'Адрес получателя',
        help_text='Адрес получателя',
        max_length=50,
    )
    close = models.BinaryField(
        'Возможность изменять заказ',
        help_text='Возможность изменять заказ',
        default=False,
    )
    products = models.ManyToManyField(
        Product,
        through='ProductOrder',
        verbose_name='Товары',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.user}, {"Закрыт" if self.close else "Не закрыт"}'


class ProductOrder(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_order',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        'Количество товара в заказе',
        help_text='Количество товара в заказе',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='product_order',
        verbose_name='Заказ',
    )

    class Meta:
        verbose_name = 'Заказ товара'
        verbose_name_plural = 'Заказы товаров'

    def __str__(self):
        return f"В {self.order} {self.quantity} {self.product}"
