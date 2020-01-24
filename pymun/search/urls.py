from django.urls import path
from .views import SearchView


urlpatterns = [
    path('', SearchView(), name='haystack_search')
]
