from django.core.exceptions import ValidationError


def get_name(value):
    for v in value:
        try:
            if type(int(v)) == int:
                raise ValidationError( 'Введите данные корректно')
        except ValueError:
            pass
