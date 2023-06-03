from collections import OrderedDict

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Car, Cargo
from .utils import (CargoService, CarService, calculate_count_of_cars,
                    get_info_about_cars)


class CargoToRepresentation:

    def to_representation(self, instance: Cargo) -> OrderedDict:
        """
        Для ответа меняем id на full_address
        """
        data = super().to_representation(instance)
        data['pick_up'] = instance.pick_up.get_full_address()
        data['delivery_to'] = instance.delivery_to.get_full_address()
        return data


class CargoInfoSerializer(CargoToRepresentation, ModelSerializer):

    cars = SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ('pick_up', 'delivery_to', 'cars')

    def get_cars(self, obj: Cargo) -> list:
        return get_info_about_cars(obj)


class CargoInfoListSerializer(CargoToRepresentation, ModelSerializer):

    count_of_cars = SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ('pick_up', 'delivery_to', 'count_of_cars')
    
    def get_count_of_cars(self, obj: Cargo) -> int:
        return calculate_count_of_cars(obj)


class CargoCreateSerializer(CargoToRepresentation, ModelSerializer):

    class Meta:
        model = Cargo
        fields = ('pick_up', 'delivery_to', 'weight', 'description')

    def validate(self, data: OrderedDict) -> OrderedDict:
        return CargoService.validate_cargo(self, data)
    
    def create(self, validated_data: dict) -> Cargo:
        return CargoService.create_cargo(self, validated_data)

    def update(self, instance: Cargo, validated_data: dict) -> Cargo:
        return CargoService.update_cargo(self, instance, validated_data)
    

class CarSerializer(ModelSerializer):

    class Meta:
        model = Car
        fields = ('plate', 'current_location', 'load_capacity')

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Достаем значения 'current_location' из не десериализованной data."""
        data['current_location'] = self.initial_data.get('current_location')
        return data

    def update(self, instance: Car, validated_data: dict) -> Car:
        return CarService.update_car(self, instance, validated_data)
    
    def to_representation(self, instance: Car) -> OrderedDict:
        """
        Для ответа меняем id на zip_index
        """
        data = super().to_representation(instance)
        data['current_location'] = instance.current_location.get_full_address()
        return data
