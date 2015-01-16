from __future__ import unicode_literals

import logging
import collections

from django.utils.translation import ugettext as _
from django.conf import settings
import django.http
import django.shortcuts
import django.views.generic.edit
import django.core.urlresolvers
import django.contrib.messages
import django.forms
from django.forms import ValidationError
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib.formtools.wizard.storage import get_storage
from django.contrib.formtools.wizard.forms import ManagementForm

import fiftythree.client

import forms


logger = logging.getLogger(__name__)

SESSION_REGISTRATION_CONFIGURATION = 'registration_configuration'
SESSION_STATE = 'data_state'
SESSION_STATE_NAME = 'data_state_name'
SESSION_EMAIL = 'data_email'
SESSION_POSTAL_CODE = 'data_postal_code'
SESSION_TOS = 'data_terms_of_service'

FIFTYTHREE_CLIENT = fiftythree.client.FiftyThreeClient(
    api_key=settings.FIFTYTHREE_CLIENT_KEY,
    endpoint=settings.FIFTYTHREE_CLIENT_ENDPOINT,
    source_url=settings.FIFTYTHREE_CLIENT_SOURCE_URL,
    use_secure=settings.FIFTYTHREE_CLIENT_USE_SECURE)


def clean_session(session):
    for key in (
            SESSION_EMAIL, SESSION_STATE, SESSION_STATE_NAME,
            SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
            SESSION_TOS):
        if key in session:
            del session[key]
    return session


class StateLookupView(django.views.generic.edit.FormView):
    template_name = 'start.html'
    form_class = forms.StateLookupForm
    success_url = django.core.urlresolvers.reverse_lazy(
        'register', kwargs={'step': '1', })

    def get(self, request, *args, **kwargs):
        clean_session(request.session)
        return super(StateLookupView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        postal_code = form.cleaned_data['postal_code']
        email = form.cleaned_data['email']

        try:
            FIFTYTHREE_CLIENT.submit_email(email, postal_code)
        except fiftythree.client.InvalidDataError as e:
            if e.message == 'Invalid email.':
                form.add_error('email', e.message)
            else:
                form.add_error('postal_code', e.message)
            django.contrib.messages.error(self.request, e.message)
            return super(StateLookupView, self).form_invalid(form)
        except fiftythree.client.ServiceError as e:
            logger.error(e.message)
            form.add_error(field=None, error=e.message)
            return super(StateLookupView, self).form_invalid(form)

        try:
            r = FIFTYTHREE_CLIENT.lookup_postal_code(postal_code)
        except fiftythree.client.InvalidDataError as e:
            django.contrib.messages.error(self.request, e.message)
            for field, errors in e.errors.items():
                for error in errors:
                    form.add_error(field, error)
            return super(StateLookupView, self).form_invalid(form)
        except fiftythree.client.ServiceError as e:
            form.add_error(field=None, error=e.message)
            return super(StateLookupView, self).form_invalid(form)

        if 'registration_configuration' not in r:
            logger.error(
                'Unknown state registration configuration: {}'.format(r))
            form.add_error(
                field=None, error='Unknown state registration configuration')
            return super(StateLookupView, self).form_invalid(form)

        # we need to show the registration form, but first we should save
        # the state and field data into the session for later use
        self.request.session[SESSION_EMAIL] = email
        self.request.session[SESSION_STATE] = r['state']
        self.request.session[SESSION_STATE_NAME] = r['state_name']
        self.request.session[SESSION_TOS] = r['terms_of_service']
        self.request.session[SESSION_POSTAL_CODE] = postal_code
        self.request.session[SESSION_REGISTRATION_CONFIGURATION] = \
            r['registration_configuration']
        return super(StateLookupView, self).form_valid(form)


class RegisterCompleteView(django.views.generic.TemplateView):
    template_name = 'register_complete.html'


class RegistrationWizardView(NamedUrlSessionWizardView):
    form_list = [forms.StateLookupForm, ]
    page_titles = collections.OrderedDict()
    page_fieldsets = collections.OrderedDict()
    page_count = 0
    configuration = None
    api_error_key = 'api_error'

    def check_configuration(self):
        if not self.configuration and \
                (SESSION_REGISTRATION_CONFIGURATION not in
                 self.request.session):
            return False
        else:
            return True

    def process_registration_configuration(self):
        self.configuration = self.request.session[
            SESSION_REGISTRATION_CONFIGURATION]

        self.page_count = len(self.configuration)
        logger.debug('process_registration_configuration: {}'.format(
            self.page_count))
        self.page_titles = collections.OrderedDict()
        self.page_fieldsets = collections.OrderedDict()
        self.form_list = collections.OrderedDict()
        for page_conf in self.configuration:
            step = unicode(page_conf['step'])
            title = page_conf['title']
            fieldsets = page_conf['fieldsets']
            if fieldsets and fieldsets[0]['fields']:
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
            # there is an error submitting the data, so pull the error data and
            # set the appropriate error on the form
            api_errors = dict(api_errors)
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
        return done_response

    def done(self, form_list, **kwargs):
        # data = {}
        # map(data.update, [form.cleaned_data for form in form_list])

        context = {
            # 'form_data': data,
            'title': 'Congratulations!'
        }
        return django.shortcuts.render_to_response(
            'formtools/wizard/done.html', context)

    def dispatch(self, request, *args, **kwargs):
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
            raise ValidationError(
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
            d['terms_of_service'] = self.request.session[SESSION_TOS]
        return d
