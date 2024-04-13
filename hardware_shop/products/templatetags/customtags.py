from django import template


register = template.Library()


@register.filter(is_safe=True)
def chunk_list(value, chunk_size=5):
    """Тег chunk_list для разбития списка по 5 элементов"""
    for i in range(0, len(value), chunk_size):
        yield value[i:i+chunk_size]
