from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, 
    RetrieveModelMixin, UpdateModelMixin, )
from rest_framework.viewsets import GenericViewSet

from .models import Car, Cargo
from .serializers import (
    CarSerializer, CargoInfoListSerializer, CargoInfoSerializer,
    CargoCreateSerializer)


class CarViewSet(UpdateModelMixin, GenericViewSet):

    queryset = Car.objects.select_related('current_location').all()
    http_method_names = ('patch',)
    serializer_class = CarSerializer


class CargoViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                    DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    
    queryset = Cargo.objects.select_related('pick_up', 'delivery_to').all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CargoInfoListSerializer
        if self.action == 'retrieve':
            return CargoInfoSerializer
        if self.action in ('create', 'partial_update'):
            return CargoCreateSerializer
