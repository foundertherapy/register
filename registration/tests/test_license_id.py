from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from forms import CharRegexField


class StateLicenseIdRegexTest(SimpleTestCase):
    def test_alabama_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='\d{7}')
        try:
            regex_field.validate('1234567')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_alaska_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_arizona_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_arkansas_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_california_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_colorado_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_delaware_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_district_of_columbia_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_hawaii_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_idaho_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_illinois_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_indiana_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_kansas_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_kentucky_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_louisiana_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_maryland_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_minnesota_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_mississippi_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_missouri_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_montana_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_new_mexico_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_north_carolina_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_north_dakota_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_ohio_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_oklahoma_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_pennsylvania_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_south_carolina_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_tennessee_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_texas_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_utah_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_washington_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_west_virginia_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)

    def test_wyoming_license_id_regex(self):
        validation_error = False
        regex_field = CharRegexField(required=True, regex='')
        try:
            regex_field.validate('')
        except ValidationError:
            validation_error = True

        self.assertFalse(validation_error)