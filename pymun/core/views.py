from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['username'] = user.username

        return context
