import os

# from bs4 import BeautifulSoup

from django.views import generic
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from xhtml2pdf import pisa

from . import models, forms
from search import forms as search_forms


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


@login_required(login_url="user-login")
def download_user_picture(request, slug):
    user = get_object_or_404(models.User, slug=slug)

    try:
        filename, extension = os.path.splitext(user.avatar.file.name)
        extension = extension[1:]
        response = FileResponse(user.avatar.file, content_type=f"image/{extension}")
        username = slugify(user.username)[:100]
        filename = slugify(user.avatar)[:100]
        response["Content-Disposition"] = "attachment; filename=" + f"{username}---{filename}.{extension}"
    except ValueError:
        response = HttpResponseNotFound(content='Picture unavailable')

    return response


@method_decorator(login_required, name='dispatch')
class ProfileView(generic.DetailView):
    model = models.User

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        # return f'context_{request.LANGUAGE_CODE}'
        return context


@method_decorator(login_required, name='dispatch')
class ManageAccountView(generic.list.ListView):
    model = models.User
    template_name = 'myaccount/manage_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class PersonalInfoView(generic.list.ListView):
    model = models.User
    template_name = 'myaccount/personal_information.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ChangeInfoView(generic.edit.UpdateView):
    model = models.User

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.object.slug})


@method_decorator(login_required, name='dispatch')
class ChangeNameView(ChangeInfoView):
    template_name = 'myaccount/change_name.html'
    form_class = forms.UpdateNameForm


@method_decorator(login_required, name='dispatch')
class ChangeBirthdayView(ChangeInfoView):
    template_name = 'myaccount/change_birthday.html'
    form_class = forms.UpdateBirthdayForm


@method_decorator(login_required, name='dispatch')
class ChangeGenderView(ChangeInfoView):
    template_name = 'myaccount/change_gender.html'
    form_class = forms.UpdateGenderForm


@method_decorator(login_required, name='dispatch')
class ChangeEmailView(generic.list.ListView):
    model = models.User
    template_name = 'myaccount/email/change_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class ChangeEmailBaseView(ChangeInfoView):
    model = models.User

    def get_context_data(self, **kwargs):
        context = super(ChangeEmailBaseView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ChangeContactEmailView(ChangeEmailBaseView):
    template_name = 'myaccount/email/change_contact_email.html'
    form_class = forms.UpdateContactEmailForm


@method_decorator(login_required, name='dispatch')
class ChangeRecoveryEmailView(ChangeEmailBaseView):
    template_name = 'myaccount/email/change_recovery_email.html'
    form_class = forms.UpdateRecoveryEmailForm


@method_decorator(login_required, name='dispatch')
class ChangeAlternateEmailView(ChangeEmailBaseView):
    template_name = 'myaccount/email/change_alternate_email.html'
    form_class = forms.UpdateAlternateEmailForm


@method_decorator(login_required, name='dispatch')
class AddAboutView(generic.list.ListView):
    model = models.User
    template_name = 'myaccount/about_me.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
