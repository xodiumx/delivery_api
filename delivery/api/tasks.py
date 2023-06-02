from random import randint

from delivery.celery import app

from .models import Car, Location


@app.task
def update_locations_of_all_cars() -> None:
    """
    Функция обновления локаций у всех автомобилей, запускается каждые 3 мин.
    """
    cars = Car.objects.all()

    locations = Location.objects.all()
    last_location_id = locations[len(locations) - 1].id

    for car in cars:
        random_id = randint(1, last_location_id)
        car.current_location = locations[random_id]

    Car.objects.bulk_update(cars, ('current_location',))
