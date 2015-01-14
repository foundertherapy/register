from __future__ import unicode_literals

import logging
import collections

from django.conf import settings
import django.http
import django.shortcuts
import django.views.generic.edit
import django.core.urlresolvers
import django.contrib.messages
import django.forms
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib.formtools.wizard.storage import get_storage

import fiftythree.client

import forms


logger = logging.getLogger(__name__)

SESSION_REGISTRATION_CONFIGURATION = 'registration_configuration'
SESSION_STATE = 'data_state'
SESSION_STATE_NAME = 'data_state_name'
SESSION_EMAIL = 'data_email'
SESSION_POSTAL_CODE = 'data_postal_code'
SESSION_TOS = 'data_terms_of_service'


class StateLookupView(django.views.generic.edit.FormView):
    template_name = 'postal_code.html'
    form_class = forms.StateLookupForm
    success_url = django.core.urlresolvers.reverse_lazy(
        'register', kwargs={'step': '1', })

    def get(self, request, *args, **kwargs):
        if SESSION_EMAIL in self.request.session:
            del self.request.session[SESSION_EMAIL]
        if SESSION_STATE in self.request.session:
            del self.request.session[SESSION_STATE]
        if SESSION_POSTAL_CODE in self.request.session:
            del self.request.session[SESSION_POSTAL_CODE]
        if SESSION_REGISTRATION_CONFIGURATION in self.request.session:
            del self.request.session[SESSION_REGISTRATION_CONFIGURATION]
        return super(StateLookupView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        c = fiftythree.client.FiftyThreeClient(
            settings.FIFTYTHREE_CLIENT_KEY,
            settings.FIFTYTHREE_CLIENT_ENDPOINT)
        postal_code = form.cleaned_data['postal_code']
        email = form.cleaned_data['email']

        try:
            c.submit_email(email, postal_code)
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
            r = c.lookup_postal_code(postal_code)
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


class RegistrationWizard(NamedUrlSessionWizardView):
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
        c = fiftythree.client.FiftyThreeClient(
            settings.FIFTYTHREE_CLIENT_KEY,
            settings.FIFTYTHREE_CLIENT_ENDPOINT)
        try:
            c.register(**data)
        except fiftythree.client.InvalidDataError as e:
            # django.contrib.messages.error(self.request, e.message)
            return e.errors.items()
        except fiftythree.client.ServiceError as e:
            # django.contrib.messages.error(self.request, e.message)
            return [[None, e.message]]

    def render_done(self, form, **kwargs):
        final_forms = collections.OrderedDict()
        # walk through the form list and try to validate the data again.
        # data = self.storage.get_step_data('4')
        # data['4-street_address'] = ''
        # print data
        # self.storage.set_step_data('4', data)

        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key))
            if not form_obj.is_valid():
                return self.render_revalidation_failure(
                    form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj

        # once forms are validated, submit the registration and render a
        # failure if submission fails
        data = {}
        map(data.update, [form.cleaned_data for form in final_forms.values()])
        # TODO: REMOVE ME
        del data['street_address']
        # TODO: END REMOVE ME
        api_errors = self.submit_registration(data)
        if api_errors:
            # there is an error submitting the data, so pull the error data and
            # set the appropriate error on the form
            api_errors = dict(api_errors)
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



        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

    def done(self, form_list, **kwargs):
        data = {}
        map(data.update, [form.cleaned_data for form in form_list])

        context = {
            'form_data': data,
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
                return django.shortcuts.redirect('home')
        return super(RegistrationWizard, self).dispatch(
            request, *args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        form_instance = super(RegistrationWizard, self).get_form(
            step, data, files)
        form_instance.api_errors = self.storage.data.get(self.api_error_key)
        return form_instance

    def get_form_initial(self, step):
        data = super(RegistrationWizard, self).get_form_initial(step)
        data['email'] = self.request.session[SESSION_EMAIL]
        data['state'] = self.request.session[SESSION_STATE]
        data['postal_code'] = self.request.session[SESSION_POSTAL_CODE]
        return data

    def get_context_data(self, form, **kwargs):
        # we should put the configuration data here...
        d = super(RegistrationWizard, self).get_context_data(form, **kwargs)
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
