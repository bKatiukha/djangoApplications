from django.core.exceptions import ValidationError
import re


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-ZА-Я]', password):
            raise ValidationError(
                "The password must contain at least 1 uppercase letter, A-Z.",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 uppercase letter, A-Z."


class DigitValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'\d', password):
            raise ValidationError(
                "The password must contain at least one digit",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Your password must contain at least one digit"
