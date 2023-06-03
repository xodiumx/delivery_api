import json
import pytest
from collections import OrderedDict

from http import HTTPStatus

from django.test.client import Client
from rest_framework.utils.serializer_helpers import ReturnDict

from api.models import Cargo


@pytest.mark.django_db(transaction=True)
class TestCargo:
    cargoes = '/api/v1/cargoes/'

    def test_00_cargoes_get(self, client: Client, cargo: Cargo) -> None:
        response = client.get(self.cargoes)
        data = response.data
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.cargoes}` не найден.'
        )
        assert isinstance(data, list), (
            f'В ответе {data} - type - {type(data)} - ожидается dict'
        )
        assert isinstance(data[0], OrderedDict), (
            f'В ответе {data[0]} - type - {type(data[0])} - '
            'ожидается OrderedDict'
        )
        assert 'pick_up' in data[0], (
            f'В {data[0]} отсутствует поле "pick_up"'
        )
        assert 'delivery_to' in data[0], (
            f'В {data[0]} отсутствует поле "delivery_to"'
        )
        assert 'count_of_cars' in data[0],(
            f'В {data[0]} отсутствует поле "count_of_cars"'
        )
        assert isinstance(data[0].get('count_of_cars'), int), (
            f'В ответе {data[0].get("count_of_cars")} - type - '
            f'{type(data[0])} - ожидается int'
        )
    
    def test_01_cargoes_get_one(self, client: Client, cargo: Cargo) -> None:
        response = client.get(f'{self.cargoes}{cargo.id}/')
        data = response.data
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.cargoes_get_one}` не найден.'
        )
        assert isinstance(data, ReturnDict), (
            f'В ответе {data} - type - {type(data)} - ожидается dict'
        )
        assert 'pick_up' in data, (
            f'В {data} отсутствует поле "pick_up"'
        )
        assert 'delivery_to' in data, (
            f'В {data} отсутствует поле "delivery_to"'
        )
        assert 'cars' in data, (
            f'В {data} отсутствует поле "cars"'
        )
        assert isinstance(data.get('cars'), list), (
            f'В ответе {data.get("cars")} - type - '
            f'{type(data.get("cars"))} - ожидается list'
        )
    
    def test_02_cargoes_post(self, client, pick_up, delivery_to):
        # TODO: add test
        ...
        
    def test_03_cargoes_patch(self, client: Client, cargo: Cargo) -> None:
        cargo_weight = cargo.weight
        cargo_description = cargo.description

        new_data = {
            'weight': 200,
            'description': 'Test description update'
        }
        response = client.patch(
            f'{self.cargoes}{cargo.id}/', 
            data=json.dumps(new_data), 
            content_type='application/json'
        )    
        assert response.status_code == HTTPStatus.OK, (
            'При изменении информации о грузе, возвращается статус 200.'
        )
        assert response.data.get('weight') != cargo_weight
        assert response.data.get('description') != cargo_description

    def test_04_cargoes_delete(self, client: Client, cargo: Cargo) -> None:
        cargo_id = cargo.id
        response = client.delete(f'{self.cargoes}{cargo_id}/')
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'При удалении груза должен возвращаться ответ со статусом 204.'
        )
        assert Cargo.objects.filter(id=cargo_id).exists() == False

        response = client.delete(f'{self.cargoes}{100}/')
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'При удалении не существуещего объекта, возвращается статус 404.'
        )
