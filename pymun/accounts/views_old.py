from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.shortcuts import redirect

from . import models

from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import forms_old as forms


class UserCreationView(CreateView):
    model = models.User
    template_name = 'registration/signup.html'
    form_class = forms.UserCreationForm
    success_url = '/accounts/login/'

    # f = forms.UserCreationForm
    # context = BeautifulSoup(f.as_p(self), features="html5lib").prettify()

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
