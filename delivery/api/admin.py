from django.contrib.admin import ModelAdmin, register

from .models import Car, Cargo, Location


@register(Location)
class LocationAdmin(ModelAdmin):
    
    list_display = ('city', 'state', 'zip_index')
    list_filter = ('city', 'state', 'zip_index')
    search_fields = ('city', 'state', 'zip_index')
    empty_value_display = '-пусто-'
    

@register(Car)
class CarAdmin(ModelAdmin):
    list_select_related = True
    
    list_display = ('plate', 'current_location', 'load_capacity', )
    list_filter = ('plate', 'current_location', 'load_capacity', )
    search_fields = ('plate', 'current_location', 'load_capacity', )
    empty_value_display = '-пусто-'


@register(Cargo)
class CargoAdmin(ModelAdmin):
    list_select_related = True

    list_display = ('pick_up', 'delivery_to', 'weight', )
    list_filter = ('pick_up', 'delivery_to', 'weight', )
    search_fields = ('pick_up', 'delivery_to', 'weight', )
    empty_value_display = '-пусто-'
