from collections import OrderedDict

from django.shortcuts import get_object_or_404

from .exceptions import SameValueException
from .models import Car, Cargo, Location


class CargoService:

    def validate_cargo(self, data: OrderedDict) -> OrderedDict:
        """
        - Достаем значения 'pick_up' и 'delivery' из не десериализованной data
        - Проверки if not, если используем update без этих полей
        """
        pick_up = self.initial_data.get('pick_up')
        delivery_to = self.initial_data.get('delivery_to')

        data['pick_up'] = pick_up
        data['delivery_to'] = delivery_to

        if not pick_up:
            data.pop('pick_up')

        if not delivery_to:
            data.pop('delivery_to')

        if pick_up and pick_up == delivery_to:
            raise SameValueException(
                {'detail': 'Одинаковое местоположение груза и доставки'})
        return data

    def create_cargo(self, validated_data: dict) -> Cargo:
        """
        Для создания, проверям есть ли локации с такими индексами в базе.
        """
        validated_data['pick_up'] = get_object_or_404(
            Location, zip_index=self.validated_data.get('pick_up'))
        validated_data['delivery_to'] = get_object_or_404(
            Location, zip_index=self.validated_data.get('delivery_to'))
        return Cargo.objects.create(**validated_data)

    def update_cargo(self, cargo: Cargo, validated_data: dict) -> Cargo:
        """
        Для обновления груза, берем новое значение из validated_data,
        если его нет берем старое из instance.
        """
        cargo.pick_up = validated_data.get('pick_up', cargo.pick_up)
        cargo.delivery_to = validated_data.get(
            'delivery_to', cargo.delivery_to)
        cargo.weight = validated_data.get('weight', cargo.weight)
        cargo.description = validated_data.get(
            'description', cargo.description)
        cargo.save()
        return cargo


class CarService:

    def update_car(self, car: Car, validated_data: dict) -> Car:
        """
        Для обновления груза, берем новое значение из validated_data,
        если его нет берем старое из instance.
        """
        current_location = validated_data.get('current_location')
        if current_location:
            car.current_location = get_object_or_404(
                Location, zip_index=current_location)
        car.plate = validated_data.get('plate', car.plate)
        car.load_capacity = validated_data.get(
            'load_capacity', car.load_capacity)
        car.save()
        return car
