from __future__ import unicode_literals

from django.conf import settings
import django.http
import django.views.generic.edit
import django.core.urlresolvers
import django.contrib.messages
import django.forms

import fiftythree.client

import forms


class StateLookupView(django.views.generic.edit.FormView):
    template_name = 'index.html'
    form_class = forms.StateLookupForm
    success_url = django.core.urlresolvers.reverse_lazy('register')

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

        if r and not r['accepts_registration']:
            return django.http.HttpResponseRedirect(r['redirect_url'])
        elif r:
            # we need to show the registration form, but first we should save
            # the state and field data into the session for later use
            self.request.session['user_email'] = email
            self.request.session['user_state'] = r['state']
            self.request.session['user_postal_code'] = postal_code
            self.request.session['form_fields'] = r['fields']
            print r['fields']
            return super(StateLookupView, self).form_valid(form)


class RegisterView(django.views.generic.edit.FormView):
    template_name = 'register.html'
    form_class = forms.RegisterForm
    success_url = django.core.urlresolvers.reverse_lazy('register_complete')

    def get(self, request, *args, **kwargs):
        # if we have a get request, we want to process the arguments passed in
        # to see if we get data overrides
        return super(RegisterView, self).get(request, *args, **kwargs)

    def get_initial(self):
        return {
            'email': self.request.session.get('user_email'),
            'postal_code': self.request.session.get('user_postal_code'),
            'state': self.request.session.get('user_state'),
        }

    def get_form(self, form_class):
        return form_class(
            fields=self.request.session.get('form_fields'), **self.get_form_kwargs())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        c = fiftythree.client.FiftyThreeClient(
            settings.FIFTYTHREE_CLIENT_KEY,
            settings.FIFTYTHREE_CLIENT_ENDPOINT)
        d = form.cleaned_data
        try:
            r = c.register(**d)
        except fiftythree.client.InvalidDataError as e:
            django.contrib.messages.error(self.request, e.message)
            for field, errors in e.errors.items():
                for error in errors:
                    form.add_error(field, error)
            return super(RegisterView, self).form_invalid(form)
        except fiftythree.client.ServiceError as e:
            form.add_error(field=None, error=e.message)
            return super(RegisterView, self).form_invalid(form)

        return super(RegisterView, self).form_valid(form)


class RegisterCompleteView(django.views.generic.TemplateView):
    template_name = 'register_complete.html'
