import pytest

from rest_framework.test import APIClient

from api.models import Car, Cargo, Location


@pytest.fixture
def user_client() -> APIClient:
    client = APIClient()
    return client


@pytest.fixture
def pick_up() -> Location:
    return Location.objects.create(
        city = 'New-York',
        state = 'New-York',
        zip_index = '10001',
        lat = 40.7,
        lng = -74.0
    )

@pytest.fixture
def delivery_to() -> Location:
    return Location.objects.create(
        city = 'Washington',
        state = 'Washington',
        zip_index = '98001',
        lat = 40.7,
        lng = -74.0
    )


@pytest.fixture
def test_car_one(pick_up: Location) -> Car:
    return Car.objects.create(
        plate = '1000A',
        current_location = pick_up,
        load_capacity = 500
    )


@pytest.fixture
def test_car_two(pick_up: Location) -> Car:
    return Car.objects.create(
        plate = '1000B',
        current_location = pick_up,
        load_capacity = 700
    )


@pytest.fixture
def cargo(pick_up: Location, delivery_to: Location) -> Cargo:
    return Cargo.objects.create(
        pick_up = pick_up,
        delivery_to = delivery_to,
        weight = 600,
        description = 'Test description',
    )
