from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CarViewSet, CargoViewSet

router_v1 = DefaultRouter()
router_v1.register('cargoes', CargoViewSet, basename='cargoes')
router_v1.register('cars', CarViewSet, basename='cars')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]