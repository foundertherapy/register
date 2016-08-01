from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


class CustomPasswordValidator(object):

    def validate(self, password, user=None):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{9,}"
        if not re.match(regex, password):
             raise ValidationError(_("This password is weak. Password should be 8 characters minimum, "
                                     "containing capital and small letters, numeric values and one of "
                                     "the following $@$!%*?&"), code='password_is_weak',)

    def get_help_text(self):
         return _("Password should be 8 characters minimum, containing capital and small letters, "
                  "numeric values and one of the following @#$%^&+=")