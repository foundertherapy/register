from __future__ import unicode_literals

import requests
import httplib


class AuthenticationError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class FiftyThreeClient(object):
    _lookup_zipcode_path = '/api/postalcodes/'
    _submit_email_path = '/api/emails/'
    _register_path = '/api/registrations/'

    def __init__(self, api_key, endpoint=None):
        self.api_key = api_key
        self.endpoint = endpoint or 'fiftythree.organize.org'

    @property
    def _headers(self):
        return {
            'Authorization': 'Token {}'.format(self.api_key),
        }

    def lookup_postal_code(self, postal_code):
        url = ''.join(
            ['http://', self.endpoint, self._lookup_zipcode_path,
             unicode(postal_code), ])
        r = requests.get(url, headers=self._headers)
        if r.status_code == httplib.OK:
            return r.json()
        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))
        elif r.status_code == httplib.NOT_FOUND:
            raise InvalidDataError('Invalid postal code.')
        else:
            print r.content

    def submit_email(self, email, postal_code):
        url = ''.join(['http://', self.endpoint, self._submit_email_path, ])
        data = {
            'email': email,
            'postal_code': unicode(postal_code),
        }
        r = requests.post(url, headers=self._headers, data=data)
        if r.status_code == httplib.OK:
            return True
        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))
        else:
            print r.content

    def register(
            self, email, first_name, last_name, birthdate, street_address,
            city, state, postal_code, license_id, middle_name=None,
            apartment=None):
        url = ''.join(['http://', self.endpoint, self._register_path, ])
        data = {
            'email': email,
            'first_name': first_name,
            'middle_name': middle_name or '',
            'last_name': last_name,
            'birthdate': unicode(birthdate),
            'street_address': street_address,
            'apartment': apartment or '',
            'city': city,
            'state': state,
            'postal_code': unicode(postal_code),
            'license_id': license_id,
        }
        r = requests.post(url, headers=self._headers, data=data)
        if r.status_code == httplib.OK:
            return True
        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))
        else:
            print r.content
