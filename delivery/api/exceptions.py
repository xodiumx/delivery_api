from rest_framework.exceptions import ValidationError


class SameValueException(ValidationError):
    ...