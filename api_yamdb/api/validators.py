import datetime
import re

from django.contrib.auth.validators import validators
from rest_framework.exceptions import ValidationError


class CorrectUsernameValidator(validators.RegexValidator):
    regex = r'^me$'
    flags = re.IGNORECASE
    inverse_match = True


def year_validate(value):
    if value > datetime.datetime.now().year:
        raise ValidationError('Недопустимый год выпуска')
