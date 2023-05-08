import re

from django.contrib.auth.validators import validators


class CorrectUsernameValidator(validators.RegexValidator):
    regex = r'^me$'
    flags = re.IGNORECASE
    inverse_match = True
