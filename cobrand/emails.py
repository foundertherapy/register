from django.conf import settings
import django.contrib.sites.models

import template_email


REGISTRATION_NOTICE_EMAIL = map(lambda x: x[1], settings.ADMINS)
FROM_ORGANIZE = 'ORGANIZE <{}>'.format(settings.DEFAULT_FROM_EMAIL)

MAILGUN_HEADERS_NO_TRACK = {
    'X-Mailgun-Track': 'no',
}


def send_admin_cobrand_register(cobrand_company):
    context = {
        'company_name': cobrand_company.company_name,
        'contact_email': cobrand_company.contact_email,
        'contact_name': cobrand_company.contact_name,
        'cobrand_url': 'http://{}{}'.format(
            django.contrib.sites.models.Site.objects.get_current().domain, cobrand_company.get_absolute_url()),
    }
    e = template_email.TemplateEmail(
        template='cobrand/emails/admin_cobrand_register.html', to=REGISTRATION_NOTICE_EMAIL, context=context,
        headers=MAILGUN_HEADERS_NO_TRACK)
    e.send()


def send_cobrand_company_register_success(cobrand_company):
    context = {
        'company_name': cobrand_company.company_name,
        'contact_email': cobrand_company.contact_email,
        'contact_name': cobrand_company.contact_name,
        'redirect_url': 'http://{}{}'.format(
            django.contrib.sites.models.Site.objects.get_current().domain, cobrand_company.get_redirect_url()),
    }

    email = template_email.TemplateEmail(
        template='cobrand/emails/cobrand_register_success.html', to=[cobrand_company.contact_email],
        from_email=FROM_ORGANIZE, context=context, headers=MAILGUN_HEADERS_NO_TRACK)
    email.send()


