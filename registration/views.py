from __future__ import unicode_literals

import logging
import collections
import datetime
import json

import dateutil.parser
import django.contrib.messages
import django.core.urlresolvers
import django.http
import django.shortcuts
import django.views.generic.edit
import django.forms
import django.utils
from django.core.cache import cache
from django.conf import settings
from formtools.wizard.forms import ManagementForm
from formtools.wizard.storage import get_storage
from formtools.wizard.views import NamedUrlSessionWizardView
from django.utils.translation import ugettext_lazy as _

import dateutil.parser

import cobrand.models
import widget.models
import fiftythree.client
import forms


logger = logging.getLogger(__name__)

SESSION_REGISTRATION_CONFIGURATION = 'registration_configuration'
SESSION_STATE = 'register_state'
SESSION_STATE_NAME = 'register_state_name'
SESSION_EMAIL = 'register_email'
SESSION_POSTAL_CODE = 'register_postal_code'
SESSION_ACCEPTS_REGISTRATION = 'register_accepts_registration'
SESSION_REDIRECT_URL = 'register_redirect_url'
SESSION_RESET_FORM = 'register_reset_form'
SESSION_REGISTRATION_UPDATE = 'registration_update'
SESSION_COBRAND_ID = 'cobrand_id'
SESSION_COBRAND_COMPANY_NAME = 'cobrand_company_name'
SESSION_COBRAND_COMPANY_LOGO = 'cobrand_company_logo'
SESSION_COBRAND_ACTIVE = 'cobrand_active'
SESSION_WIDGET_ID = 'widget_id'
SESSION_WIDGET_HOST_URL = 'widget_host_url'
SESSION_REG_SOURCE = 'reg_source'
SESSION_VARIANT_ID = 'variant_id'
SESSION_REGISTRATION_UUID = 'registration_uuid'
SESSION_FIRST_NAME = 'first_name'
SESSION_LICENSE_ID_FORMATS = 'license_id_formats'
SESSION_UPENN_REGISTRATION = 'is_upenn_registration'


COOKIE_MINOR = 'register_minor'

FIFTYTHREE_CLIENT = fiftythree.client.FiftyThreeClient(
    api_key=settings.FIFTYTHREE_CLIENT_KEY,
    endpoint=settings.FIFTYTHREE_CLIENT_ENDPOINT,
    source_url=settings.FIFTYTHREE_CLIENT_SOURCE_URL,
    use_secure=settings.FIFTYTHREE_CLIENT_USE_SECURE)

FIFTYTHREE_CLIENT.lookup_zipcode_api_path(api_version='v3')


def clean_session(session):
    for key in (
            SESSION_STATE, SESSION_STATE_NAME, SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
            SESSION_ACCEPTS_REGISTRATION, SESSION_REDIRECT_URL, SESSION_REGISTRATION_UPDATE,
            SESSION_LICENSE_ID_FORMATS, SESSION_UPENN_REGISTRATION, ):
        if key in session:
            del session[key]
    session[SESSION_RESET_FORM] = True
    return session


def clean_email_source_session(session):
    for key in (SESSION_REG_SOURCE, SESSION_VARIANT_ID, ):
        if key in session:
            del session[key]
    return session


def clean_cobrand_session(session):
    for key in (SESSION_COBRAND_COMPANY_NAME, SESSION_COBRAND_COMPANY_LOGO, SESSION_COBRAND_ACTIVE, SESSION_COBRAND_ID, ):
        if key in session:
            del session[key]
    return session


def clean_widget_session(session):
    for key in (SESSION_WIDGET_HOST_URL, SESSION_WIDGET_ID, ):
        if key in session:
            del session[key]
    return session


def clean_next_of_kin_email_session(session):
    for key in (SESSION_REGISTRATION_UUID, SESSION_FIRST_NAME, SESSION_EMAIL, ):
        if key in session:
            del session[key]
    return session


def get_external_source_data(session):
    external_source_data = {}
    for key in (
            SESSION_COBRAND_COMPANY_NAME, SESSION_COBRAND_ID, SESSION_WIDGET_HOST_URL, SESSION_WIDGET_ID,
            SESSION_REG_SOURCE, SESSION_VARIANT_ID, ):
        if key in session:
            external_source_data[key] = session[key]
    return external_source_data


def setup_external_source_session(request):
    cobrand_id = request.GET.get('cobrand_id')
    widget_id = request.GET.get('widget_id')
    reg_source = request.GET.get('reg_source')
    variant_id = request.GET.get('variant_id')

    if cobrand_id:
        try:
            clean_widget_session(request.session)
            clean_email_source_session(request.session)

            company_name = cache.get('cobrand:{}'.format(cobrand_id))
            if not company_name:
                cobrand_company = cobrand.models.CobrandCompany.objects.get(uuid=cobrand_id)
                company_name = cobrand_company.company_name
                cache.set('cobrand:{}'.format(cobrand_id), company_name, 60 * 60 * 24)

            request.session[SESSION_COBRAND_ACTIVE] = True
            request.session[SESSION_COBRAND_ID] = cobrand_id
            request.session[SESSION_COBRAND_COMPANY_LOGO] = '{}.png'.format(cobrand_id)
            request.session[SESSION_COBRAND_COMPANY_NAME] = company_name
        except cobrand.models.CobrandCompany.DoesNotExist:
            pass
    elif widget_id:
        try:
            clean_cobrand_session(request.session)
            clean_email_source_session(request.session)
            widget_host = widget.models.WidgetHost.objects.get(uuid=widget_id)
            request.session[SESSION_WIDGET_ID] = widget_id
            request.session[SESSION_WIDGET_HOST_URL] = widget_host.host_url
        except widget.models.WidgetHost.DoesNotExist:
            pass
    elif reg_source:
        clean_cobrand_session(request.session)
        clean_widget_session(request.session)
        request.session[SESSION_REG_SOURCE] = reg_source
        request.session[SESSION_VARIANT_ID] = variant_id
    else:
        # Clean widget session only if no external source params exist in the URL, because widget params are the only that we
        # don't want to keep for returning users, unless widget_id is in the URL.
        clean_widget_session(request.session)


def strip_unicode_from_list(unicode_list):
    stripped_list = [str(unicode_item) for unicode_item in unicode_list]
    return stripped_list


class UserCheckMixin(object):
    user_check_failure_path = ''  # can be path, url name or reverse_lazy

    def check_user(self, request, user):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        return django.shortcuts.redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request, request.user):
            return self.user_check_failed(request, *args, **kwargs)
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class MinorRestrictedMixin(UserCheckMixin):
    user_check_failure_path = 'register_minor'
    permission_required = None

    def check_user(self, request, user):
        return request.COOKIES.get(COOKIE_MINOR) != 'true'

    def render_restricted_minor_registration(self):
        """
        This method gets called when we receive an error that we are trying to
        register a minor. This should set a cookie that prevents additional
        attempts at registration, and should redirect to the appropriate error
        page.
        """
        response = django.shortcuts.redirect('register_minor')
        response.set_cookie(
            COOKIE_MINOR, 'true', expires=datetime.datetime(2033, 1, 1),
            secure=False, httponly=True)
        return response


class StateLookupView(MinorRestrictedMixin, django.views.generic.edit.FormView):
    template_name = 'registration/start.html'
    form_class = forms.StateLookupForm
    accepts_registration = True

    def get(self, request, *args, **kwargs):
        clean_session(request.session)
        clean_next_of_kin_email_session(request.session)
        setup_external_source_session(request)
        return super(StateLookupView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        if self.accepts_registration:
            return django.core.urlresolvers.reverse(
                'register', kwargs={'step': '1', })
        else:
            return django.core.urlresolvers.reverse('unsupported_state')

    def get_initial(self):
        initial = self.initial.copy()
        if 'email' in self.request.GET:
            initial['email'] = self.request.GET['email']
        if 'postal_code' in self.request.GET:
            initial['postal_code'] = self.request.GET['postal_code']
        return initial

    def get_context_data(self, **kwargs):
        data = super(StateLookupView, self).get_context_data(**kwargs)
        data['update'] = self.is_update
        if data['update']:
            data['page_title'] = _('Update your registration')
        else:
            data['page_title'] = _('Let&rsquo;s Begin...')

        return data

    @property
    def is_update(self):
        return self.kwargs.get('update') is True

    def submit_email(self, data):
        data_copy = data.copy()
        data_copy.update(get_external_source_data(self.request.session))
        FIFTYTHREE_CLIENT.submit_email(**data_copy)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        try:
            self.submit_email(form.cleaned_data)
        except fiftythree.client.InvalidDataError as e:
            if e.message == 'Invalid email.':
                form.add_error('email', _(e.message))
            else:
                form.add_error('postal_code', _(e.message))
            logger.error('{} While trying to call EmailSubmit API '
                         'with error response {}'.format(e.message, unicode(e.errors)))
            django.contrib.messages.error(self.request, _(e.message))
            return self.form_invalid(form)
        except fiftythree.client.ServiceError as e:
            logger.error(e.message)
            form.add_error(field=None, error=_(e.message))
            return self.form_invalid(form)

        postal_code = form.cleaned_data['postal_code']
        email = form.cleaned_data['email']

        try:
            postal_code_response = cache.get('postal_code_data:{}'.format(postal_code))
            if not postal_code_response:
                postal_code_response = FIFTYTHREE_CLIENT.lookup_postal_code(postal_code)
                cache.set('postal_code_data:{}'.format(postal_code),
                          postal_code_response, settings.POSTAL_CODE_RESPONSE_CACHE_TIMEOUT)
        except fiftythree.client.InvalidDataError as e:
            django.contrib.messages.error(self.request, _(e.message))
            for field, errors in e.errors.items():
                for error in errors:
                    form.add_error(field, _(error))
            logger.error('{} While trying to call PostalCode lookup API '
                         'with error response {}'.format(e.message, unicode(e.errors)))
            return self.form_invalid(form)
        except fiftythree.client.ServiceError as e:
            form.add_error(field=None, error=_(e.message))
            return self.form_invalid(form)

        if 'registration_configuration' not in postal_code_response:
            logger.error(
                'Unknown state registration configuration: {}'.format(postal_code_response))
            form.add_error(
                field=None, error=_('Unknown state registration configuration'))
            return self.form_invalid(form)

        self.request.session[SESSION_EMAIL] = email
        self.request.session[SESSION_STATE] = postal_code_response['state']
        self.request.session[SESSION_STATE_NAME] = postal_code_response['state_name']
        self.request.session[SESSION_POSTAL_CODE] = postal_code
        self.request.session[SESSION_REGISTRATION_UPDATE] = self.is_update

        if 'license_id_formats' in postal_code_response:
            self.request.session[SESSION_LICENSE_ID_FORMATS] = postal_code_response['license_id_formats']

        if postal_code_response['accepts_registration']:
            self.accepts_registration = True
            self.request.session[SESSION_ACCEPTS_REGISTRATION] = True
            self.request.session[SESSION_REDIRECT_URL] = ''
            self.request.session[SESSION_REGISTRATION_CONFIGURATION] = \
                postal_code_response['registration_configuration']
        else:
            self.accepts_registration = False
            self.request.session[SESSION_ACCEPTS_REGISTRATION] = False
            self.request.session[SESSION_REDIRECT_URL] = postal_code_response['redirect_url']

        return super(StateLookupView, self).form_valid(form)


class UPENNStateLookupView(StateLookupView):
    form_class = forms.UPENNStateLookupForm

    def get(self, request, *args, **kwargs):
        res = super(UPENNStateLookupView, self).get(request, *args, **kwargs)
        request.session[SESSION_UPENN_REGISTRATION] = '1'
        return res


class UnsupportedStateView(django.views.generic.TemplateView):
    template_name = 'registration/unsupported_state.html'

    def get(self, request, *args, **kwargs):
        # if we don't have a session variable set for a state redirect,
        # send the user back to 'start'
        redirect_url = self.request.session.get(SESSION_REDIRECT_URL)
        if not redirect_url:
            return django.shortcuts.redirect('start')
        context = self.get_context_data(**kwargs)
        context['state'] = self.request.session[SESSION_STATE]
        context['state_name'] = self.request.session[SESSION_STATE_NAME]
        return self.render_to_response(context)


class StateRedirectView(django.views.generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # if we have a redirect_url defined, get it and redirect
        redirect_url = self.request.session.get(SESSION_REDIRECT_URL)
        # kill the session data since we want to reset the user flow
        clean_session(self.request.session)
        if redirect_url:
            return redirect_url
        else:
            return django.core.urlresolvers.reverse('start')


class RegistrationWizardView(MinorRestrictedMixin, NamedUrlSessionWizardView):
    form_list = [forms.StateLookupForm, ]
    page_titles = collections.OrderedDict()
    page_fieldsets = collections.OrderedDict()
    page_explanatory_texts = collections.OrderedDict()
    page_count = 0
    configuration = None
    api_error_key = 'api_error'

    def check_configuration(self):
        if not self.configuration and (SESSION_REGISTRATION_CONFIGURATION not in self.request.session):
            return False
        else:
            return True

    def process_registration_configuration(self):
        self.configuration = self.request.session[SESSION_REGISTRATION_CONFIGURATION]
        license_id_formats = None
        if SESSION_LICENSE_ID_FORMATS in self.request.session:
            license_id_formats = self.request.session[SESSION_LICENSE_ID_FORMATS]

        self.page_count = len(self.configuration)
        logger.debug('process_registration_configuration: {}'.format(self.page_count))
        self.page_titles = collections.OrderedDict()
        self.page_fieldsets = collections.OrderedDict()
        self.form_list = collections.OrderedDict()
        for page_conf in self.configuration:
            step = unicode(page_conf['step'])
            title = _(page_conf['title'])
            explanatory_text = page_conf['explanatory_text']
            fieldsets = page_conf['fieldsets']
            if license_id_formats:
                page_conf['license_id_formats'] = license_id_formats
            if fieldsets and \
                    any([fieldset['fields'] for fieldset in fieldsets]):
                logging.debug('Processing step {}: {}'.format(step, title))
                self.page_titles[step] = title
                self.page_explanatory_texts[step] = explanatory_text
                self.page_fieldsets[step] = fieldsets
                self.form_list[unicode(step)] = forms.register_form_generator(
                    conf=page_conf)

    def submit_registration(self, data):
        try:
            data_copy = data.copy()
            data_copy.update(get_external_source_data(self.request.session))
            uuid = FIFTYTHREE_CLIENT.register(**data_copy)
            logger.info('Register successful: {}'.format(uuid))
            self.request.session[SESSION_REGISTRATION_UUID] = uuid
            self.request.session[SESSION_FIRST_NAME] = data_copy['first_name']
        except fiftythree.client.InvalidDataError as e:
            logger.error('{} While trying to call Register API '
                         'with error response {}'.format(e.message, unicode(e.errors)))
            return e.errors.items()
        except fiftythree.client.ServiceError as e:
            logger.error(e.message)
            return [[None, e.message]]
        except fiftythree.client.AuthenticationError as e:
            logger.error(e.message)
            return [[None, e.message]]

    def render_done(self, form, **kwargs):
        final_forms = collections.OrderedDict()
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key))
            # if there are api_errors, when re-validating this any form we want
            # to skip api error validation because we're going to do it again
            # below
            form_obj.skip_api_error_validation = True
            if not form_obj.is_valid():
                return self.render_revalidation_failure(
                    form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj

        # once forms are validated, submit the registration and render a
        # failure if submission fails
        data = {}
        map(data.update, [form.cleaned_data for form in final_forms.values()])
        api_errors = self.submit_registration(data)
        if api_errors:
            api_errors_dict = dict(api_errors)
            # check to see if we have an error with a minor registering
            if 'non_field_errors' in api_errors_dict.keys():
                non_field_errors = api_errors_dict['non_field_errors']
                if 'Minors cannot register.' in non_field_errors:
                    self.storage.reset()
                    return self.render_restricted_minor_registration()

            # there is an error submitting the data, so pull the error data and
            # set the appropriate error on the form
            # call ugettext on the list of errors for each
            api_errors_dict = {a: [django.utils.translation.ugettext(c) for c in b]
                          for a, b in api_errors_dict.items()}
            logger.warning('Received API errors for postal_code {}: {}'.format(
                data['postal_code'], api_errors_dict))
            self.storage.data[self.api_error_key] = api_errors_dict
            for form_key in self.get_form_list():
                form_obj = self.get_form(
                    step=form_key,
                    data=self.storage.get_step_data(form_key),
                    files=self.storage.get_step_files(form_key))
                last_form_key = form_key
                last_form_obj = form_obj
                error_field_names = set(form_obj.fields.keys()).intersection(
                    set(api_errors_dict.keys()))
                if error_field_names:
                    form_obj.add_error(field=None, error=api_errors_dict)
                    return self.render_revalidation_failure(form_key, form_obj, **kwargs)

            if api_errors[0][0] is None:
                last_form_obj.add_error(field=None, error=[api_errors[0][1]])
                #return self.render_revalidation_failure(last_form_key, last_form_obj, **kwargs)
                return self.render_to_response(self.get_context_data(form=form, errors=api_errors[0][1]))

            logger.critical(
                    'API errors not properly handled by forms for postal_code {}: {}'.format(data['postal_code'], api_errors))


        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()
        # also clean out the session
        clean_session(self.request.session)
        # I Don't think we need to clear those session values on registration done, as it is going to be cleared on the
        # next visit for Start page anyways.
        # clean_cobrand_session(self.request.session)
        # clean_widget_session(self.request.session)
        # clean_email_source_session(self.request.session)
        return done_response

    def done(self, form_list, **kwargs):
        if self.request.session[SESSION_REGISTRATION_UPDATE]:
            return django.shortcuts.redirect('update_done')
        else:
            return django.shortcuts.redirect('email_next_of_kin')

    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get(COOKIE_MINOR) == 'true':
            return django.shortcuts.redirect('register_minor')

        if request.session.get(SESSION_RESET_FORM):
            del request.session[SESSION_RESET_FORM]
            prefix = self.get_prefix(request, *args, **kwargs)
            storage = get_storage(self.storage_name, prefix, request,
                                  getattr(self, 'file_storage', None))
            storage.reset()
        if not self.configuration:
            if self.check_configuration():
                self.process_registration_configuration()
            else:
                prefix = self.get_prefix(request, *args, **kwargs)
                storage = get_storage(self.storage_name, prefix, request,
                                      getattr(self, 'file_storage', None))
                storage.reset()
                # we are missing registration configuration,
                # so send the user back
                return django.shortcuts.redirect('start')
        return super(RegistrationWizardView, self).dispatch(
            request, *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Do a redirect if user presses the prev. step button. The rest of this
        is super'd from WizardView.
        """
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)

        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)

        # Check if form was refreshed
        management_form = ManagementForm(self.request.POST, prefix=self.prefix)
        if not management_form.is_valid():
            raise django.forms.ValidationError(
                _('ManagementForm data is missing or has been tampered.'),
                code='missing_management_form',
            )

        form_current_step = management_form.cleaned_data['current_step']
        if (form_current_step != self.steps.current and
                self.storage.current_step is not None):
            # form refreshed, change current step
            self.storage.current_step = form_current_step

        # get the form for the current step
        form = self.get_form(data=self.request.POST, files=self.request.FILES)
        # THIS IS THE BIG CHANGE TO SUPPORT API VALIDATION ERRORS
        # if there are api_errors, when the user re-submits the form, we want to
        # skip api error validation for this form
        form.skip_api_error_validation = True

        # and try to validate
        if form.is_valid():
            # if the form is valid, store the cleaned data and files.
            self.storage.set_step_data(self.steps.current, self.process_step(form))
            self.storage.set_step_files(self.steps.current, self.process_step_files(form))

            # check if the current step is the last step
            if self.steps.current == self.steps.last:
                # no more steps, render done view
                return self.render_done(form, **kwargs)
            else:
                # proceed to the next step
                return self.render_next_step(form)
        return self.render(form)

    def get_form(self, step=None, data=None, files=None):
        form_instance = super(RegistrationWizardView, self).get_form(
            step, data, files)
        form_instance.api_errors = self.storage.data.get(self.api_error_key)
        return form_instance

    def get_form_initial(self, step):
        data = super(RegistrationWizardView, self).get_form_initial(step)
        data['email'] = self.request.session[SESSION_EMAIL]
        data['state'] = self.request.session[SESSION_STATE]
        data['postal_code'] = self.request.session[SESSION_POSTAL_CODE]
        return data

    def get_context_data(self, form, **kwargs):
        # we should put the configuration data here...
        d = super(RegistrationWizardView, self).get_context_data(form, **kwargs)
        d['title'] = self.page_titles[self.steps.current]
        d['explanatory_text'] = self.page_explanatory_texts[self.steps.current]
        d['state'] = self.request.session[SESSION_STATE]
        d['state_name'] = self.request.session[SESSION_STATE_NAME]
        d['postal_code'] = self.request.session[SESSION_POSTAL_CODE]
        d['email'] = self.request.session[SESSION_EMAIL]

        current_form = self.form_list[unicode(self.steps.current)]
        if 'license_id' in current_form.base_fields:
            if SESSION_LICENSE_ID_FORMATS in self.request.session:
                license_id_formats = strip_unicode_from_list(
                    self.request.session[SESSION_LICENSE_ID_FORMATS])
                d['license_id_formats'] = json.dumps(license_id_formats)
                invalid_license_modal_content = {
                    'title': _('Please check your license ID'),
                    'body': _('The license ID you entered doesn&rsquo;t seem to match the format of license IDs '
                              'for this State. Please double-check it, and if you&rsquo;re sure its right, '
                              'please choose to continue.'),
                    'ok': _('Continue to Next Page'),
                    'cancel': _('Re-check License ID'), }
                d['invalid_license_modal_content'] = invalid_license_modal_content

        if self.steps.current == self.steps.last:
            d['cleaned_data'] = self.get_all_cleaned_data()
            self.configuration = filter(lambda item: item['title'] != 'Confirm your information',
                                        self.configuration)

            d['configuration'] = self.configuration

        d['non_field_errors'] = kwargs.get('errors')

        return d


class ResetMinorCookieDocument(django.views.generic.RedirectView):
    pattern_name = 'start'

    def get(self, request, *args, **kwargs):
        response = super(ResetMinorCookieDocument, self).get(
            request, *args, **kwargs)
        response.delete_cookie(COOKIE_MINOR)
        return response


class LegalDocument(django.views.generic.TemplateView):
    template_name = 'registration/legal_document.html'
    title = 'Legal Document'
    api_name = None

    def get_document(self):
        return FIFTYTHREE_CLIENT.document(self.api_name)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['title'] = self.title
        try:
            r = self.get_document()
            context['content'] = r['content']
            context['hash'] = r['hash']
            context['active_on'] = dateutil.parser.parse(r['active_on'])
        except fiftythree.client.InvalidDataError as e:
            logger.error('{} While trying to call Document API '
                         'with error response {}'.format(e.message, unicode(e.errors)))
        except fiftythree.client.ServiceError as e:
            logger.error(e.message)

        return self.render_to_response(context)


class TermsOfServiceView(LegalDocument):
    title = 'Terms of Service'
    api_name = 'terms-of-service'


class PrivacyPolicyView(LegalDocument):
    title = 'Privacy Policy'
    api_name = 'privacy-policy'


class TermsOfServiceByStateView(LegalDocument):
    title = 'State-by-State Terms of Service'
    api_name = 'terms-of-service-by-state'


class RevokeView(MinorRestrictedMixin, django.views.generic.edit.FormView):
    template_name = 'registration/revoke.html'
    postal_code = ''
    form_class = forms.RevokeForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # email = form.cleaned_data['email']
        # postal_code = form.cleaned_data['postal_code']
        # first_name = form.cleaned_data['first_name']
        # middle_name = form.cleaned_data['middle_name']
        # last_name = form.cleaned_data['last_name']
        # birthdate = form.cleaned_data['birthdate']

        api_errors = self.submit_deregistration(form.cleaned_data)

        if api_errors:
            api_errors = dict(api_errors)
            # check to see if we have an error with a minor registering
            if 'non_field_errors' in api_errors.keys():
                non_field_errors = api_errors['non_field_errors']
                if 'Minors cannot register.' in non_field_errors:
                    return self.render_restricted_minor_registration()

            api_errors = {a: [django.utils.translation.ugettext(c) for c in b]
                          for a, b in api_errors.items()}
            logger.error(
                'Received API errors for registration: {}'.format(api_errors))
            error_field_names = set(form.fields.keys()).intersection(set(api_errors.keys()))
            if error_field_names:
                form.add_error(field=None, error=api_errors)
                return self.form_invalid(form)

        # if the form is valid, set the postal_code
        self.postal_code = form.cleaned_data['postal_code']

        return super(RevokeView, self).form_valid(form)

    def get_success_url(self):
        if self.postal_code:
            return django.core.urlresolvers.reverse_lazy(
                'revoke_done', kwargs={'postal_code': self.postal_code, })
        else:
            return django.core.urlresolvers.reverse_lazy('revoke-done')

    def submit_deregistration(self, data):
        try:
            data_copy = data.copy()
            data_copy.update(get_external_source_data(self.request.session))
            FIFTYTHREE_CLIENT.revoke(**data_copy)
        except fiftythree.client.InvalidDataError as e:
            logger.error('{} While trying to call Revoke '
                         'API with error response {}'.format(e.message, unicode(e.errors)))
            return e.errors.items()
        except fiftythree.client.ServiceError as e:
            logger.error(e.message)
            return [[None, e.message]]
        except fiftythree.client.AuthenticationError as e:
            logger.error(e.message)
            return [[None, e.message]]


class RevokeDoneView(django.views.generic.TemplateView):
    template_name = 'registration/revoke_done.html'
    title = _('Donor Registration Revocation Complete')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['title'] = self.title
        if 'postal_code' in self.kwargs:
            try:
                r = FIFTYTHREE_CLIENT.lookup_postal_code(
                    self.kwargs['postal_code'])
                context['registry_url'] = r.get('registry_url')
            except fiftythree.client.InvalidDataError as e:
                logger.error('{} While trying to call PostalCode '
                             'API for revocation complete with error response {}'.format(e.message, unicode(e.errors)))
            except fiftythree.client.ServiceError as e:
                logger.error(e.message)

        return self.render_to_response(context)


class EmailNextOfKinView(MinorRestrictedMixin, django.views.generic.FormView):
    template_name = 'registration/email_next_of_kin.html'
    form_class = forms.EmailNextOfKinForm
    initial = {
        'subject': _("Just wanted to let you know, I'm an official organ donor!"),
        'body': _("""FYI: I just registered to be an organ donor on ORGANIZE because I dig the idea of saving someone else's life. I'm now legally registered, but my next of kin (which is YOU) will still be asked to uphold my decision. So, here you go: I WANT TO BE AN ORGAN DONOR.

If you want to register too, it takes less than a minute on ORGANIZE.org.

This email probably felt out of the blue and might have made you uncomfortable. Get over it! This is really important.

Your hero,

{}
"""),
    }

    def get(self, request, *args, **kwargs):
        # make sure we have a registration_uuid
        if SESSION_REGISTRATION_UUID not in self.request.session:
            # there isn't enough information to offer a NOK email, so just redirect to done
            return django.shortcuts.redirect('done')
        return super(EmailNextOfKinView, self).get(self, request, *args, **kwargs)

    def get_initial(self):
        initial = super(EmailNextOfKinView, self).get_initial()
        initial['body'] = initial['body'].format(self.request.session.get(SESSION_FIRST_NAME, '[YOUR NAME HERE]'))
        return initial

    def get_context_data(self, **kwargs):
        context = super(EmailNextOfKinView, self).get_context_data(**kwargs)
        context['inverse_logo'] = True
        return context

    def get_success_url(self):
        return django.core.urlresolvers.reverse_lazy('done')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        api_errors = self.submit_nok_email(form.cleaned_data)

        if api_errors:
            api_errors = {a: [django.utils.translation.ugettext(c) for c in b] for a, b in dict(api_errors).items()}
            logger.error('Received API errors for registration: {}'.format(api_errors))
            error_non_field_names = []
            for field_name, error in api_errors.items():
                if field_name in form.fields.keys():
                    form.add_error(field=field_name, error=error)
                else:
                    error_non_field_names.append(error)
            if error_non_field_names:
                form.add_error(field=None, error=error_non_field_names)
            return self.form_invalid(form)

        return super(EmailNextOfKinView, self).form_valid(form)

    def submit_nok_email(self, data):
        try:
            data_copy = data.copy()
            data_copy['from_email'] = self.request.session.get(SESSION_EMAIL, settings.DEFAULT_FROM_EMAIL)
            if SESSION_REGISTRATION_UUID in self.request.session:
                data_copy['registration_uuid'] = self.request.session[SESSION_REGISTRATION_UUID]
            else:
                django.contrib.messages.add_message(self.request, django.contrib.messages.INFO, 'Registration required.')
                return [[None, ['Registration ID required.']]]
            FIFTYTHREE_CLIENT.email_next_of_kin(**data_copy)
        except fiftythree.client.InvalidDataError as e:
            logger.error('{} While trying to call EmailNextOfKin API '
                         'with error response {}'.format(e.message, unicode(e.errors)))
            return e.errors.items()
        except fiftythree.client.ServiceError as e:
            logger.error(e.message)
            return [[None, e.message]]
        except fiftythree.client.AuthenticationError as e:
            logger.error(e.message)
            return [[None, e.message]]


class RegisterDoneView(MinorRestrictedMixin, django.views.generic.TemplateView):
    template_name = 'registration/done.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterDoneView, self).get_context_data(**kwargs)
        context['inverse_logo'] = True
        return context

