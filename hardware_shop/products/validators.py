from django.core.exceptions import ValidationError


def validate_score(value):
    if value < 0:
        raise ValidationError(
            ('Оценка должна быть положительной'),
        )
