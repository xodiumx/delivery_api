from delivery.celery import app

from .models import Car, random_location


@app.task
def update_locations_of_all_cars():
    """
    Функция обновления локаций у всех автомобилей, запускается каждые 3 мин.
    """
    cars = Car.objects.all()
    for car in cars:
        car.current_location = random_location()
    Car.objects.bulk_update(cars, ('current_location',))
