from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from forms import CharRegexField


class StateLicenseIdRegexTest(SimpleTestCase):
    def test_state_license_id_regex(self):
        validation_error = False
        valid_regex_field = CharRegexField(required=True, regex='\d{7}')
        try:
            valid_regex_field.validate('1234567')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

        validation_error = False
        invalid_regex_field = CharRegexField(required=True, regex='')
        try:
            invalid_regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertTrue(validation_error)
