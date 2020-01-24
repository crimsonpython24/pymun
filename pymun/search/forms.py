from __future__ import absolute_import, division, print_function, unicode_literals

from django import forms
from django.utils.encoding import smart_text
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from haystack.utils import get_model_ct
from haystack.utils.app_loading import haystack_get_model


def model_choices(using=DEFAULT_ALIAS):
    choices = [
        (get_model_ct(m), capfirst(smart_text(m._meta.verbose_name_plural)))
        for m in connections[using].get_unified_index().get_indexed_models()
    ]
    return sorted(choices, key=lambda x: x[1])


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_("Search"), widget=forms.TextInput(attrs={"type": "search"}))

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop("searchqueryset", None)
        self.load_all = kwargs.pop("load_all", False)

        if self.searchqueryset is None: self.searchqueryset = SearchQuerySet()
        super(SearchForm, self).__init__(*args, **kwargs)

    @staticmethod
    def no_query_found():
        return EmptySearchQuerySet()

    def search(self):
        if not self.is_valid(): return self.no_query_found()
        if not self.cleaned_data.get("q"): return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data["q"])
        if self.load_all: sqs = sqs.load_all()
        return sqs

    def get_suggestion(self):
        if not self.is_valid(): return None
        return self.searchqueryset.spelling_suggestion(self.cleaned_data["q"])


class ModelSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(ModelSearchForm, self).__init__(*args, **kwargs)
        self.fields["models"] = forms.MultipleChoiceField(
            choices=model_choices(),
            required=False,
            label=_("Search In"),
            widget=forms.CheckboxSelectMultiple,
        )

    def get_models(self):
        search_models = []
        if self.is_valid():
            for model in self.cleaned_data["models"]:
                search_models.append(haystack_get_model(*model.split(".")))

        return search_models

    def search(self):
        sqs = super(ModelSearchForm, self).search()
        return sqs.models(*self.get_models())
