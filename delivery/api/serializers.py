from django.shortcuts import get_object_or_404

from rest_framework.serializers import (
    ImageField, ModelSerializer, PrimaryKeyRelatedField, ReadOnlyField,
    Serializer, SerializerMethodField, CharField, IntegerField
)

from .exceptions import SameValueException
from .models import Car, Cargo, Location


class CargoInfoSerializer(ModelSerializer):

    class Meta:
        model = Cargo
        fields = ('pick_up', 'delivery_to') # TODO: counts aoto


class CargoCreateSerializer(ModelSerializer):

    class Meta:
        model = Cargo
        fields = ('pick_up', 'delivery_to', 'weight', 'description')

    def validate(self, data):
        """
        Достаем значения 'pick_up' и 'delivery' 
        из не десериализованной data
        """
        data['pick_up'] = self.initial_data.get('pick_up')
        data['delivery_to'] = self.initial_data.get('delivery_to')
        
        if data.get('pick_up') == data.get('delivery_to'):
            raise SameValueException(
                {'detail': 'Одинаковое местоположение груза и доставки'})
        return data
    
    def create(self, validated_data):
        """
        Для создания, проверям есть ли локации с такими индексами в базе.
        """
        validated_data['pick_up'] = get_object_or_404(
            Location, zip_index=self.validated_data.get('pick_up'))
        validated_data['delivery_to'] = get_object_or_404(
            Location, zip_index=self.validated_data.get('delivery_to'))
        return Cargo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Для обновления груза, берем новое значение из validated_data, 
        если его нет берем старое из instance.
        """
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """
        Для ответа меняем id на zip_index
        """
        data = super().to_representation(instance)
        data['pick_up'] = str(instance.pick_up)
        data['delivery_to'] = str(instance.delivery_to)
        return data


class CarSerializer(ModelSerializer):

    class Meta:
        model = Car
        fields = ('plate', 'current_location', 'load_capacity')
    
    def validate(self, data):
        """Достаем значения 'current_location' из не десериализованной data."""
        data['current_location'] = self.initial_data.get('current_location')
        return data

    def update(self, instance, validated_data):
        """
        Для обновления груза, берем новое значение из validated_data, 
        если его нет берем старое из instance.
        """
        current_location = validated_data.get('current_location')
        if current_location:
            instance.current_location = get_object_or_404(
                Location, zip_index=current_location)      
        instance.plate = validated_data.get('plate', instance.plate)
        instance.load_capacity = validated_data.get(
            'load_capacity', instance.load_capacity)
        return instance
    
    def to_representation(self, instance):
        """
        Для ответа меняем id на zip_index
        """
        data = super().to_representation(instance)
        data['current_location'] = str(instance.current_location)
        instance.save()
        return data
