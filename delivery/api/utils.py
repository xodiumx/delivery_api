from geopy import distance

from .models import Car


DISTANCE_DIFF = 450


def calculate_count_of_cars(cargo):
    """
    Функция расчета количества ближайших автомобилей до груза (макс. 450 миль).
    """
    cargo_coordinates = (cargo.pick_up.lat, cargo.pick_up.lng)
    count = 0
    cars = []
    for car in Car.objects.all():
        car_coordinates = car.current_location.lat, car.current_location.lng
        dist = distance.distance(cargo_coordinates, car_coordinates).miles
        if dist <= DISTANCE_DIFF:
            count += 1
            cars.append(car.id)
    return count


def get_info_about_cars(cargo):
    """
    Получения информации о автомобилях:
        - plate: автомобильный номер
        - distance: расстояние от автомобиля до груза
    """
    cargo_coordinates = (cargo.pick_up.lat, cargo.pick_up.lng)
    cars = []
    for car in Car.objects.all():
        car_info = {}
        car_info['plate'] = car.plate

        car_coordinates = car.current_location.lat, car.current_location.lng
        dist = distance.distance(cargo_coordinates, car_coordinates).miles

        car_info['distance'] = f'{dist:.2f} miles'
        cars.append(car_info)

    return cars
