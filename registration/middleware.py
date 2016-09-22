import django.middleware.locale
import django.shortcuts
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class RequestLocaleMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # first check to see if we have a language specified as a GET parameter
        if request.method == 'GET':
            language = request.GET.get('lang')
            if language:
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = translation.get_language()
                query = request.GET.copy()
                del query['lang']
                path = '?'.join([request.path, query.urlencode()])
                return django.shortcuts.redirect(path)
