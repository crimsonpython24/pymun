
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . import forms
from haystack.query import EmptySearchQuerySet

RESULTS_PER_PAGE = getattr(settings, "HAYSTACK_SEARCH_RESULTS_PER_PAGE", 20)


@csrf_exempt
class SearchView(object):
    template = "search/search.html"
    extra_context = {}
    query = ""
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None, searchqueryset=None, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.searchqueryset = searchqueryset

        if form_class is None:
            self.form_class = forms.SearchForm

        if results_per_page is not None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        self.request = request
        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        data = None
        kwargs = {"load_all": self.load_all}
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs["searchqueryset"] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        if self.form.is_valid():
            return self.form.cleaned_data["q"]

        return ""

    def get_results(self):
        return self.form.search()

    def build_page(self):
        try:
            page_no = int(self.request.GET.get("page", 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        var = self.results[start_offset: start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return paginator, page

    @staticmethod
    def extra_context():
        return {}

    def get_context(self) -> object:
        (paginator, page) = self.build_page()

        context = {
            "query": self.query,
            "form": self.form,
            "page": page,
            "paginator": paginator,
            "suggestion": None,
        }

        if hasattr(self.results, "query") and self.results.query.backend.include_spelling:
            context["suggestion"] = self.form.get_suggestion()

        context.update(self.extra_context())

        return context

    def create_response(self):
        context = self.get_context()

        return render(self.request, self.template, context)
