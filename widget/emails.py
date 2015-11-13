from django.conf import settings
import django.contrib.sites.models

import template_email


REGISTRATION_NOTICE_EMAIL = map(lambda x: x[1], settings.ADMINS)
FROM_ORGANIZE = 'ORGANIZE <{}>'.format(settings.DEFAULT_FROM_EMAIL)

MAILGUN_HEADERS_NO_TRACK = {
    'X-Mailgun-Track': 'no',
}


def send_admin_widget_register(widget_host):
    context = {
        'uuid': widget_host.uuid,
        'host_url': widget_host.host_url,
        'contact_email': widget_host.contact_email,
        'contact_name': widget_host.contact_name,
        'widget_url': 'http://{}{}'.format(
            django.contrib.sites.models.Site.objects.get_current().domain, widget_host.get_absolute_url()),
    }
    e = template_email.TemplateEmail(
        template='widget/emails/admin_widget_register.html', to=REGISTRATION_NOTICE_EMAIL, context=context,
        headers=MAILGUN_HEADERS_NO_TRACK)
    e.send()


def send_widget_register_success(widget_host):
    context = {
        'uuid': widget_host.uuid,
        'host_url': widget_host.host_url,
        'contact_email': widget_host.contact_email,
        'contact_name': widget_host.contact_name,
        'widget_url': 'http://{}{}'.format(
            django.contrib.sites.models.Site.objects.get_current().domain, widget_host.get_absolute_url()),
    }

    email = template_email.TemplateEmail(
        template='widget/emails/widget_register_success.html', to=[widget_host.contact_email],
        from_email=FROM_ORGANIZE, context=context, headers=MAILGUN_HEADERS_NO_TRACK)
    email.send()


