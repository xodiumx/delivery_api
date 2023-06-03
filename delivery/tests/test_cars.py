import json
import pytest

from http import HTTPStatus


@pytest.mark.django_db(transaction=True)
class TestCar:
    cars = '/api/v1/cars/'

    def test_00_test_car_patch(self, client, test_car_one, delivery_to):
        # TODO: add test
        ...