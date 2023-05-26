from delivery.celery import app

from .models import Car, random_location


@app.task
def update_locations_of_all_cars():
    """
    Функция обновления локаций у всех автомобилей, запускается каждые 3 мин.
    """
    for car in Car.objects.all():
        car.current_location = random_location()
        car.save()
