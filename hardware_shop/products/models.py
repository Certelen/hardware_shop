from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        help_text='Название категории',
        max_length=50,
    )
    description = models.TextField(
        'Описание категории',
        help_text='Описание категории',
    )
    image = models.ImageField(
        'Изображение категории',
        upload_to='categorys_img/',
        help_text='Изображение категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'Название товара',
        help_text='Название товара',
        max_length=50,
    )
    description = models.TextField(
        'Описание товара',
        help_text='Описание товара',
    )
    main_image = models.ImageField(
        'Изображение товара в превью',
        upload_to='products_img/',
        help_text='Изображение товара в превью',
    )
    characteristic = models.TextField(
        'Характеристики товара',
        help_text='Характеристики товара',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='Категория товара',
    )
    company = models.CharField(
        'Компания производящая товар',
        help_text='Название компании',
        max_length=50,
    )
    quantity = models.PositiveIntegerField(
        'Количество остатка товара',
        help_text='Количество остатка товара',
        default=0
    )
    price = models.PositiveIntegerField(
        'Цена товара',
        help_text='Цена товара',
        default=0
    )
    score = models.PositiveIntegerField(
        'Оценка товара',
        help_text='Оценка товара',
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    created = models.DateTimeField(
        'Дата добавления товара',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Изображения товара',
    )
    image = models.ImageField(
        'Изображение товара',
        upload_to='products_img/',
        help_text='Загрузка картинки'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
