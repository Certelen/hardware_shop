import unidecode


def category_image_directory_path(instance, filename):
    """Путь для изображений категорий"""
    return f'category_img/{unidecode.unidecode(filename)}'


def product_main_image_directory_path(instance, filename):
    """Путь для главного изображения товара"""
    return f'products_img/{instance.id}/{unidecode.unidecode(filename)}'


def product_images_directory_path(instance, filename):
    """Путь для других изображений товара"""
    return f'products_img/{instance.product.id}/{unidecode.unidecode(filename)}'
