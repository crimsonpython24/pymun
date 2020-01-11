from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('signup/', views.UserCreationView.as_view(), name='signup'),
    # path('edit_main/<slug:slug>', views.EditMainView.as_view(), name='edit_main'),
    # path('edit_addons/<slug:slug>', views.EditAddonsView.as_view(), name='edit_addons'),

    path('profile/<slug:slug>', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:slug>/pdf/', views.download_cv_pdf, name="user-pdf"),

    path('<slug:slug>/myaccount', views.ManageAccountView.as_view(), name='my_account'),
    path('<slug:slug>/myaccount/personal-info', views.PersonalInfoView.as_view(), name='personal_info'),
    path('<slug:slug>/myaccount/change_name', views.ChangeNameView.as_view(), name='change_name'),
    path('<slug:slug>/myaccount/change_birthday', views.ChangeBirthdayView.as_view(), name='change_birthday'),
    path('<slug:slug>/myaccount/change_gender', views.ChangeGenderView.as_view(), name='change_gender'),
    path('<slug:slug>/myaccount/change_email', views.ChangeEmailView.as_view(), name='change_email')
]
