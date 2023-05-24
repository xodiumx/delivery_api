from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, 
    RetrieveModelMixin, UpdateModelMixin, )
from rest_framework.viewsets import GenericViewSet

from .models import Car, Cargo
from .serializers import (
    CarSerializer, CargoInfoSerializer, CargoCreateSerializer)


class CargoViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                    DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    
    queryset = Cargo.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CargoInfoSerializer
        if self.action in ('create', 'partial_update'):
            return CargoCreateSerializer
        

class CarViewSet(UpdateModelMixin, GenericViewSet):
    queryset = Car.objects.all()
    http_method_names = ('patch',)
    serializer_class = CarSerializer