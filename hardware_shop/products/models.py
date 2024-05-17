from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import products.validate as validator


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
        upload_to=validator.category_image_directory_path,
        help_text='Изображение категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class CategoryChar(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='char',
        verbose_name='Характеристики категории',
    )
    characteristic_name = models.CharField(
        'Название характеристики',
        max_length=200
    )

    class Meta:
        verbose_name = 'Харатеристики категории'
        verbose_name_plural = 'Харатеристика категории'

    def __str__(self):
        return f'{self.characteristic_name} категории {self.category.name}'


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='Категория товара',
    )
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
        upload_to=validator.product_main_image_directory_path,
        help_text='Изображение товара в превью',
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


class ProductChar(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='char',
        verbose_name='Характеристики товара',
    )
    characteristic_name = models.CharField(
        'Название характеристики',
        max_length=200
    )
    characteristic_value = models.CharField(
        'Значение характеристики',
        max_length=200
    )

    class Meta:
        verbose_name = 'Харатеристики товара'
        verbose_name_plural = 'Харатеристики товаров'

    def __str__(self):
        return f'{self.characteristic_name} товара {self.product.name}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Изображения товара',
    )
    image = models.ImageField(
        'Изображение товара',
        upload_to=validator.product_images_directory_path,
        help_text='Загрузка картинки'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
