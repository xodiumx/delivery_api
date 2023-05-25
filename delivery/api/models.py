from random import randint

from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

MIN_WEIGHT_OF_CARGO = 1
MAX_WEIGHT_OF_CARGO = 1000
MAX_LENGTH_OF_CARGO_DESCRIPTION = 500
CARGO_ZIP_MAX_LENGTH = 5
CAR_PLATE_LENGTH = 5
CAR_PLATE_MIN_NUMBER = 1000
CAR_PLATE_MAX_NUMBER = 9999
CAR_PLATE_PATTERN = r'[1-9][0-9]{3}[A-Z]$'


def random_location():
    """Функция получения рандомной локации для создания автомобиля."""
    random_id = randint(1, Location.objects.latest('id').id)
    return Location.objects.get(id=random_id)


class Location(models.Model):
    """
    Model Location:
    Attributes:
        - city: Название города
        - state: Название штата
        - zip_index: Почтовый индекс
        - lat: Широта
        - lng: Долгота
    """
    city = models.CharField(
        'Город',
        max_length=100,
        db_index=True,
        null=False,
        blank=False,
    )
    state = models.CharField(
        'Штат',
        max_length=100,
        db_index=True,
        null=False,
        blank=False,
    )
    zip_index = models.CharField(
        'Почтовый индекс',
        max_length=10,
        db_index=True,
        null=False,
        blank=False,
    )
    lat = models.CharField(
        'Широта',
        max_length=20,
        db_index=True,
        null=False,
        blank=False,
    )
    lng = models.CharField(
        'Долгота',
        max_length=20,
        db_index=True,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ('city',)
    
    def __str__(self):
        return self.zip_index
    
    def get_full_address(self):
        return f'{self.city} {self.state} {self.zip_index}'


class Car(models.Model):
    """
    Model Car:
    Attributes:
        - plate: автомобильный номер.
        - current_location: локация где находится автомобиль.
        - load_capacity: грузоподъемность автомобиля.
    """
    plate = models.CharField(
        'Автомобильный номер',
        max_length=CAR_PLATE_LENGTH,
        unique=True,
        validators=(
            RegexValidator(
                CAR_PLATE_PATTERN,
                message=f'Формат номера: число от {CAR_PLATE_MIN_NUMBER} '
                        f'до {CAR_PLATE_MAX_NUMBER} плюс '
                        f'одна латинская буква в конце'),
        )
    )
    current_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        default=random_location,
        db_index=True,
        related_name='where_car',
        verbose_name='Текущая локация',
    )
    load_capacity = models.IntegerField(
        'Грузоподъемность',
        null=False,
        blank=False,
        validators=(
            MaxValueValidator(
                MAX_WEIGHT_OF_CARGO,
                message=f'Максимальный вес груза {MAX_WEIGHT_OF_CARGO}'),
            MinValueValidator(
                MIN_WEIGHT_OF_CARGO,
                message=f'Минимальный вес груза {MIN_WEIGHT_OF_CARGO}')
        ),
    )

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return self.plate


class Cargo(models.Model):
    """
    Model Cargo:
    Attributes:
        - pick_up: локация от куда забирать.
        - delivery_to: локация куда доставлять.
        - weight: вес груза
        - description: описание груза
    """
    pick_up = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='wherefrom',
        verbose_name='Откуда',
    )
    delivery_to = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='to_where',
        verbose_name='Куда',
    )
    weight = models.IntegerField(
        'Вес груза',
        null=False,
        blank=False,
        validators=(
            MaxValueValidator(
                MAX_WEIGHT_OF_CARGO,
                message=f'Максимальный вес груза {MAX_WEIGHT_OF_CARGO}'),
            MinValueValidator(
                MIN_WEIGHT_OF_CARGO,
                message=f'Минимальный вес груза {MIN_WEIGHT_OF_CARGO}')
        ),
    )
    description = models.TextField(
        'Описание',
        max_length=MAX_LENGTH_OF_CARGO_DESCRIPTION,
        null=False,
        blank=False
    )

    def __str__(self):
        return f'Груз {self.id}'

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        ordering = ('-id',)
