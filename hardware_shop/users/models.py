from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UnicodeUsernameValidator,
    Group,
    Permission
)
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

from products.models import Product
from .managers import UserManager

order_status = [
    ('0', 'Не оформлен пользователем'),
    ('1', 'В работе'),
    ('2', 'Отправлен'),
    ('3', 'Отменён'),
]


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    username_validator = UnicodeUsernameValidator()

    favorite_products = models.ManyToManyField(
        Product,
        related_name='users',
        verbose_name='Избранные товары',
        blank=True
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_(
            "150 characters or fewer."
        ),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    birth_date = models.DateField(
        "Дата рождения",
        null=True,
        blank=True
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
        blank=True
    )

    phone = models.CharField(
        "Номер телефона",
        max_length=15,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.email

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        """
        Автоматическое создание группы Менеджер
        """
        super(CustomUser, self).save(
            force_insert, force_update, *args, **kwargs)
        if not Group.objects.filter(name='Менеджер'):
            order_permissions = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(Order)
            )
            order_permissions = order_permissions.filter(
                Q(codename='view_order') | Q(codename='change_order')
            )
            manager = Group.objects.create(
                name='Менеджер'
            )
            manager.permissions.add(*order_permissions)


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Пользователь оставивший отзыв',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Товар на который оставляется отзыв',
    )
    title = models.CharField(
        'Заголовок отзыва',
        help_text='Заголовок отзыва',
        max_length=50,
    )
    comment = models.TextField(
        'Текст отзыва',
        help_text='Текст отзыва',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка товара',
        help_text='Оценка товара',
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.title


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
        max_length=15,
        blank=True
    )
    address = models.CharField(
        'Адрес получателя',
        help_text='Адрес получателя',
        max_length=50,
        blank=True
    )
    close = models.CharField(
        'Статус заказа',
        max_length=50,
        default=0,
        choices=order_status
    )
    products = models.ManyToManyField(
        Product,
        through='ProductOrder',
        verbose_name='Товары',
    )
    close_data = models.DateField(
        "Дата закрытия заказа",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.user}, {self.get_close_display()}'

    @receiver(post_save, sender=CustomUser)
    def create_first_user_order(sender, instance, created, **kwargs):
        if created:
            Order.objects.create(user=instance)


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
