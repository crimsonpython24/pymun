import os

# from bs4 import BeautifulSoup

from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.text import slugify
from xhtml2pdf import pisa
from crispy_forms.helper import FormHelper

from . import models, forms


def link_callback(uri, rel):
    # convert URIs to absolute system paths
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        # handle absolute uri (ie: http://my.tld/a.png)
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            "Media URI must start with "
            f"'{settings.STATIC_URL}' or '{settings.MEDIA_URL}'")
    return path


def download_cv_pdf(request, slug):
    user = get_object_or_404(models.User, slug=slug)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={slugify(user, True)}.pdf"

    html = render_to_string("accounts/user_pdf.html", {"user": user})
    status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if status.err:
        response = HttpResponseServerError("The PDF could not be generated.")

    return response


@method_decorator(login_required, name='dispatch')
class ProfileView(generic.DetailView):
    model = models.User

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        # return f'context_{request.LANGUAGE_CODE}'
        return context


@method_decorator(login_required, name='dispatch')
class ManageAccountView(generic.detail.DetailView):
    model = models.User
    template_name = 'myaccount/manage_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class PersonalInfoView(generic.detail.DetailView):
    model = models.User
    template_name = 'myaccount/personal_information.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ChangeInfoView(generic.edit.UpdateView):
    model = models.User
    template_name = 'myaccount/change_name.html'
    form_class = forms.UserUpdateNameForm

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.object.slug})


@method_decorator(login_required, name='dispatch')
class ChangeNameView(ChangeInfoView):
    template_name = 'myaccount/change_name.html'
    form_class = forms.UserUpdateNameForm


@method_decorator(login_required, name='dispatch')
class ChangeGenderView(ChangeInfoView):
    template_name = 'myaccount/change_gender.html'
    form_class = forms.UserUpdateGenderForm
