from __future__ import unicode_literals

import logging
import collections
import datetime

import dateutil.parser
import django.contrib.messages
import django.core.urlresolvers
import django.http
import django.shortcuts
import django.views.generic.edit
import django.forms
from django.conf import settings
from django.contrib.formtools.wizard.forms import ManagementForm
from django.contrib.formtools.wizard.storage import get_storage
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

import dateutil.parser

import cobrand.models
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
SESSION_COBRAND_COMPANY_NAME = 'cobrand_company_name'
SESSION_COBRAND_COMPANY_LOGO = 'cobrand_company_logo'
SESSION_COBRAND_ACTIVE = 'cobrand_active'

COOKIE_MINOR = 'register_minor'

FIFTYTHREE_CLIENT = fiftythree.client.FiftyThreeClient(
    api_key=settings.FIFTYTHREE_CLIENT_KEY,
    endpoint=settings.FIFTYTHREE_CLIENT_ENDPOINT,
    source_url=settings.FIFTYTHREE_CLIENT_SOURCE_URL,
    use_secure=settings.FIFTYTHREE_CLIENT_USE_SECURE)


def clean_session(session):
    for key in (
            SESSION_EMAIL, SESSION_STATE, SESSION_STATE_NAME, SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
            SESSION_ACCEPTS_REGISTRATION, SESSION_REDIRECT_URL, SESSION_REGISTRATION_UPDATE, ):
        if key in session:
            del session[key]
    session[SESSION_RESET_FORM] = True
    return session


def clean_cobrand(session):
    for key in (SESSION_COBRAND_COMPANY_NAME, SESSION_COBRAND_COMPANY_LOGO, SESSION_COBRAND_ACTIVE, ):
        if key in session:
            del session[key]
    return session


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


class CobrandCheckMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cobrand_id = self.request.GET.get('cobrand_id')

        if cobrand_id:
            try:
                cobrand_company = cobrand.models.CobrandCompany.objects.get(uuid=cobrand_id)
                request.session[SESSION_COBRAND_ACTIVE] = True
                request.session[SESSION_COBRAND_COMPANY_LOGO] = '{}.png'.format(cobrand_company.uuid)
                request.session[SESSION_COBRAND_COMPANY_NAME] = cobrand_company.company_name
            except cobrand.models.CobrandCompany.DoesNotExist:
                pass

        return super(CobrandCheckMixin, self).dispatch(request, *args, **kwargs)


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


class StateLookupView(MinorRestrictedMixin, CobrandCheckMixin, django.views.generic.edit.FormView):
    template_name = 'registration/start.html'
    form_class = forms.StateLookupForm
    accepts_registration = True

    def get(self, request, *args, **kwargs):
        clean_session(request.session)
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

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        postal_code = form.cleaned_data['postal_code']
        email = form.cleaned_data['email']

        try:
            FIFTYTHREE_CLIENT.submit_email(email, postal_code)
        except fiftythree.client.InvalidDataError as e:
            if e.message == 'Invalid email.':
                form.add_error('email', _(e.message))
            else:
                form.add_error('postal_code', _(e.message))
            django.contrib.messages.error(self.request, _(e.message))
            return super(StateLookupView, self).form_invalid(form)
        except fiftythree.client.ServiceError as e:
            logger.error(e.message)
            form.add_error(field=None, error=_(e.message))
            return super(StateLookupView, self).form_invalid(form)

        try:
            r = FIFTYTHREE_CLIENT.lookup_postal_code(postal_code)
        except fiftythree.client.InvalidDataError as e:
            django.contrib.messages.error(self.request, _(e.message))
            for field, errors in e.errors.items():
                for error in errors:
                    form.add_error(field, _(error))
            return super(StateLookupView, self).form_invalid(form)
        except fiftythree.client.ServiceError as e:
            form.add_error(field=None, error=_(e.message))
            return super(StateLookupView, self).form_invalid(form)

        if 'registration_configuration' not in r:
            logger.error(
                'Unknown state registration configuration: {}'.format(r))
            form.add_error(
                field=None, error=_('Unknown state registration configuration'))
            return super(StateLookupView, self).form_invalid(form)

        self.request.session[SESSION_EMAIL] = email
        self.request.session[SESSION_STATE] = r['state']
        self.request.session[SESSION_STATE_NAME] = r['state_name']
        self.request.session[SESSION_POSTAL_CODE] = postal_code
        self.request.session[SESSION_REGISTRATION_UPDATE] = self.is_update

        if r['accepts_registration']:
            self.accepts_registration = True
            self.request.session[SESSION_ACCEPTS_REGISTRATION] = True
            self.request.session[SESSION_REDIRECT_URL] = ''
            self.request.session[SESSION_REGISTRATION_CONFIGURATION] = \
                r['registration_configuration']
        else:
            self.accepts_registration = False
            self.request.session[SESSION_ACCEPTS_REGISTRATION] = False
            self.request.session[SESSION_REDIRECT_URL] = r['redirect_url']

        return super(StateLookupView, self).form_valid(form)


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
    permanent = False

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

        self.page_count = len(self.configuration)
        logger.debug('process_registration_configuration: {}'.format(self.page_count))
        self.page_titles = collections.OrderedDict()
        self.page_fieldsets = collections.OrderedDict()
        self.form_list = collections.OrderedDict()
        for page_conf in self.configuration:
            step = unicode(page_conf['step'])
            title = _(page_conf['title'])
            fieldsets = page_conf['fieldsets']
            if fieldsets and \
                    any([fieldset['fields'] for fieldset in fieldsets]):
                logging.debug('Processing step {}: {}'.format(step, title))
                self.page_titles[step] = title
                self.page_fieldsets[step] = fieldsets
                self.form_list[unicode(step)] = forms.register_form_generator(
                    conf=page_conf)

    def submit_registration(self, data):
        try:
            FIFTYTHREE_CLIENT.register(**data)
        except fiftythree.client.InvalidDataError as e:
            logger.error(e.message)
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
            api_errors = dict(api_errors)
            # check to see if we have an error with a minor registering
            if 'non_field_errors' in api_errors.keys():
                non_field_errors = api_errors['non_field_errors']
                if 'Minors cannot register.' in non_field_errors:
                    self.storage.reset()
                    return self.render_restricted_minor_registration()

            # there is an error submitting the data, so pull the error data and
            # set the appropriate error on the form
            # call ugettext on the list of errors for each
            api_errors = {a: [ugettext(c) for c in b]
                          for a, b in api_errors.items()}
            logger.error('Received API errors for postal_code {}: {}'.format(
                data['postal_code'], api_errors))
            self.storage.data[self.api_error_key] = api_errors
            for form_key in self.get_form_list():
                form_obj = self.get_form(
                    step=form_key,
                    data=self.storage.get_step_data(form_key),
                    files=self.storage.get_step_files(form_key))
                error_field_names = set(form_obj.fields.keys()).intersection(
                    set(api_errors.keys()))
                if error_field_names:
                    # process the date error as a special case for translation
                    # because it has a variable
                    # for k, v in api_errors.items():
                    #     print v
                    #     if v.startswith('Date must be later than'):
                    #         v_start, v_end = v.split('than ')
                    #         v_end = v_end.replace('.')
                    #         date_error = dateutil.parser.parse(v_end)
                    #         api_errors[k] = _(''.join([v_start, '%(date)s'])) \
                    #                         % {'date': date_error, }
                    #         break

                    form_obj.add_error(
                        field=None, error=api_errors)
                    return self.render_revalidation_failure(
                        form_key, form_obj, **kwargs)
            logger.critical(
                'API errors not properly handled by forms for postal_code {}: '
                '{}'.format(data['postal_code'], api_errors))

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_forms.values(),
                                  form_dict=final_forms, **kwargs)
        self.storage.reset()
        # also clean out the session
        clean_session(self.request.session)
        clean_cobrand(self.request.session)
        return done_response

    def done(self, form_list, **kwargs):
        if self.request.session[SESSION_REGISTRATION_UPDATE]:
            return django.shortcuts.redirect('update_done')
        else:
            return django.shortcuts.redirect('done')

    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get(COOKIE_MINOR) == 'true':
            return django.shortcuts.redirect('register_minor')

        if request.session.get(SESSION_RESET_FORM):
            del request.session[SESSION_RESET_FORM]
            prefix = self.get_prefix(*args, **kwargs)
            storage = get_storage(self.storage_name, prefix, request,
                                  getattr(self, 'file_storage', None))
            storage.reset()
        if not self.configuration:
            if self.check_configuration():
                self.process_registration_configuration()
            else:
                prefix = self.get_prefix(*args, **kwargs)
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
        d['state'] = self.request.session[SESSION_STATE]
        d['state_name'] = self.request.session[SESSION_STATE_NAME]
        d['postal_code'] = self.request.session[SESSION_POSTAL_CODE]
        d['email'] = self.request.session[SESSION_EMAIL]

        if self.steps.current == self.steps.last:
            d['cleaned_data'] = self.get_all_cleaned_data()
            d['configuration'] = self.configuration

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
            logger.error(e.message)
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

            api_errors = {a: [ugettext(c) for c in b]
                          for a, b in api_errors.items()}
            logger.error(
                'Received API errors for registration: {}'.format(api_errors))
            error_field_names = set(form.fields.keys()).intersection(
                set(api_errors.keys()))
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
            FIFTYTHREE_CLIENT.revoke(**data)
        except fiftythree.client.InvalidDataError as e:
            logger.error(e.message)
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
                logger.error(e.message)
            except fiftythree.client.ServiceError as e:
                logger.error(e.message)

        return self.render_to_response(context)
