from django.urls import path
from .views import SearchView, AdminListView


urlpatterns = [
    path('', SearchView(), name='haystack_search'),
    path('admin/', AdminListView.as_view(), name='search_list_admins')
]
