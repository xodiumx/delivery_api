from rest_framework.exceptions import ValidationError


class WeightException(ValidationError):
    ...


class SameValueException(ValidationError):
    ...