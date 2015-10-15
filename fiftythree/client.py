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
    def __init__(
            self, api_key, endpoint=None, source_url=None, api_version='v2',
            use_secure=True):
        self.api_key = api_key
        self.endpoint = endpoint or 'fiftythree.organize.org'
        self.api_version = api_version
        self.source_url = source_url or \
                          'https://register.organize.org/'
        self.use_secure = use_secure
        if use_secure:
            self.scheme = 'https://'
        else:
            self.scheme = 'http://'
        self.lookup_zipcode_path = '/api/{}/postal-codes/'.format(api_version)
        self.submit_email_path = '/api/{}/emails/'.format(api_version)
        self.register_path = '/api/{}/registrations/'.format(api_version)
        self.revoke_path = '/api/{}/revocations/'.format(api_version)

    @property
    def _headers(self):
        return {
            'Authorization': 'Token {}'.format(self.api_key),
        }

    def lookup_postal_code(self, postal_code):
        url = ''.join(
            [self.scheme, self.endpoint, self.lookup_zipcode_path,
             unicode(postal_code), '/', ])
        try:
            r = requests.get(url, headers=self._headers)
        except requests.ConnectionError as e:
            logger.error(e)
            raise ServiceError('Service unavailable.')

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

        elif r.status_code in (
                httplib.SERVICE_UNAVAILABLE, httplib.INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def submit_email(self, email, postal_code, subscribe_to_email_list=False):
        url = ''.join([self.scheme, self.endpoint, self.submit_email_path, ])
        data = {
            'email': email,
            'postal_code': unicode(postal_code),
            'subscribe_to_email_list': subscribe_to_email_list,
            'source_url': self.source_url
        }
        try:
            r = requests.post(url, headers=self._headers, data=data)
        except requests.ConnectionError as e:
            logger.error(e)
            raise ServiceError('Service unavailable.')

        if r.status_code == httplib.OK:
            return True

        elif r.status_code == httplib.CREATED:
            logger.info('Successfully submitted email')

        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == httplib.UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == httplib.BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                httplib.SERVICE_UNAVAILABLE, httplib.INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def register(self, **data):
        url = ''.join([self.scheme, self.endpoint, self.register_path, ])
        data['source_url'] = self.source_url
        r = requests.post(url, headers=self._headers, data=data)

        if r.status_code == httplib.OK:
            return True

        elif r.status_code in (httplib.METHOD_NOT_ALLOWED, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == httplib.UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == httplib.BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                httplib.SERVICE_UNAVAILABLE, httplib.INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        elif r.status_code == httplib.CREATED:
            logger.info('Successfully submitted registration')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def revoke(self, **data):
        url = ''.join([self.scheme, self.endpoint, self.revoke_path, ])
        data['source_url'] = self.source_url
        r = requests.post(url, headers=self._headers, data=data)

        if r.status_code == httplib.OK:
            return r.json

        elif r.status_code in (httplib.METHOD_NOT_ALLOWED, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == httplib.UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == httplib.BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                httplib.SERVICE_UNAVAILABLE, httplib.INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        elif r.status_code == httplib.CREATED:
            logger.info('Successfully submitted revocation')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False

    def document(self, name):
        url = ''.join(
            [self.scheme, self.endpoint, '/api/v2/', name, '/'])
        try:
            r = requests.get(url, headers=self._headers)
        except requests.ConnectionError as e:
            logger.error(e)
            raise ServiceError('Service unavailable.')

        if r.status_code == httplib.OK:
            return r.json()

        elif r.status_code in (httplib.UNAUTHORIZED, httplib.FORBIDDEN, ):
            raise AuthenticationError(r.json().get('detail'))

        elif r.status_code == httplib.NOT_FOUND:
            raise InvalidDataError('No Document Available.', {})

        elif r.status_code == httplib.UNPROCESSABLE_ENTITY:
            raise InvalidDataError(r.json().get('detail'), {})

        elif r.status_code == httplib.BAD_REQUEST:
            raise InvalidDataError('Invalid data.', r.json())

        elif r.status_code in (
                httplib.SERVICE_UNAVAILABLE, httplib.INTERNAL_SERVER_ERROR):
            raise ServiceError('Service unavailable.')

        else:
            logger.info('Unknown status code: {}'.format(r.status_code))
            return False
