import os

from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.text import slugify
from xhtml2pdf import pisa

from . import models, forms



def link_callback(uri, rel):
    # convert URIs to absolute system paths
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
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


class UserCreationView(CreateView):
    model = models.User
    template_name = 'registration/signup.html'
    form_class = forms.UserCreationForm
    success_url = '/accounts/login/'


class ProfileView(generic.DetailView):
    model = models.User

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        # return f'context_{request.LANGUAGE_CODE}'
        return context


@method_decorator(login_required, name='dispatch')
class EditMainView(UpdateView):
    model = models.User
    form_class = forms.UserUpdateFormMain
    template_name = 'accounts/edit_main.html'

    @staticmethod
    def add_image(request):
        form = forms.UserUpdateFormMain()
        if request.user.is_authenticated():
            if request.method == 'GET':
                context = {'user': request.user}
                return render(request, 'accounts/edit_main.html', context)
            elif request.method == 'POST':
                form = forms.UserUpdateFormMain(data=request.POST, files=request.FILES)

            if form.is_valid():
                form.save()
                request.user.save()
                print('\nvalid!')
                return redirect('index')
            else:
                context = {'user': request.user, 'form': form}
                print('\ninvalid otherwise')
                return render(request, 'accounts/edit_main.html', context)
        else:
            return HttpResponse('Unauthorized', status=401)

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.object.slug})


@method_decorator(login_required, name='dispatch')
class EditAddonsView(UpdateView):
    model = models.User
    form_class = forms.UserUpdateFormAddons
    template_name = 'accounts/edit_addons.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.object.slug})
