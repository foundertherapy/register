from __future__ import unicode_literals

import requests
import httplib
import logging


logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    pass


class ServiceError(Exception):
    pass


class InvalidDataError(Exception):
    def __init__(self, message, errors):
        self.errors = errors
        self.message = message


class FiftyThreeClient(object):

    def __init__(self, api_key, endpoint=None, api_version='v1'):
        self.api_key = api_key
        self.endpoint = endpoint or 'fiftythree.organize.org'
        self.api_version = api_version
        self.lookup_zipcode_path = '/api/{}/postal-codes/'.format(api_version)
        self.submit_email_path = '/api/{}/emails/'.format(api_version)
        self.register_path = '/api/{}/registrations/'.format(api_version)

    @property
    def _headers(self):
        return {
            'Authorization': 'Token {}'.format(self.api_key),
        }

    def lookup_postal_code(self, postal_code):
        url = ''.join(
            ['http://', self.endpoint, self.lookup_zipcode_path,
             unicode(postal_code), '/', ])
        r = requests.get(url, headers=self._headers)

        if r.status_code == httplib.OK:
            return r.json()

        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == httplib.NOT_FOUND:
            raise InvalidDataError(
                'Invalid postal code.',
                {'postal_code': ['Invalid postal code.']})

        elif r.status_code == httplib.UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == httplib.BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code == httplib.SERVICE_UNAVAILABLE:
            raise ServiceError('Service unavailable.')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def submit_email(self, email, postal_code):
        url = ''.join(['http://', self.endpoint, self.submit_email_path, ])
        data = {
            'email': email,
            'postal_code': unicode(postal_code),
        }
        r = requests.post(url, headers=self._headers, data=data)

        if r.status_code == httplib.OK:
            return True

        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == httplib.UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == httplib.BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code == httplib.SERVICE_UNAVAILABLE:
            raise ServiceError('Service unavailable.')

        elif r.status_code == httplib.CREATED:
            logger.info('Successfully submitted email')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def register(
            self, email, first_name, last_name, birthdate, street_address,
            city, state, postal_code, license_id, middle_name=None,
            apartment=None):
        url = ''.join(['http://', self.endpoint, self.register_path, ])
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
            'source': 'http://fiftythree-dev.herokuapp.com/register/',
        }
        r = requests.post(url, headers=self._headers, data=data)

        if r.status_code == httplib.OK:
            return True

        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == httplib.UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == httplib.BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code == httplib.SERVICE_UNAVAILABLE:
            raise ServiceError('Service unavailable.')

        elif r.status_code == httplib.CREATED:
            logger.info('Successfully submitted registration')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False
