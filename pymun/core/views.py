from django.views import generic

from search import forms as search_forms


class IndexView(generic.FormView):
    template_name = "base.html"

    form_class = search_forms.SearchForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['username'] = user.username

        return context
