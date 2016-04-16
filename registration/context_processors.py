import django.conf


def settings(request):
    # adds a few important settings to context variables
    return {
        'FACEBOOK_APP_ID': django.conf.settings.FACEBOOK_APP_ID,
    }
