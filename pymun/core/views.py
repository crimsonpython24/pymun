from django.views import generic

from accounts.models import User


class IndexView(generic.TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context
