from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('signup/', views.UserCreationView.as_view(), name='signup'),
    # path('edit_main/<slug:slug>', views.EditMainView.as_view(), name='edit_main'),
    # path('edit_addons/<slug:slug>', views.EditAddonsView.as_view(), name='edit_addons'),

    path('myaccount/', views.ManageAccountView.as_view(), name='my_account'),
    path('myaccount/personal_info', views.PersonalInfoView.as_view(), name='personal_info'),
    path('myaccount/change_name', views.ChangeNameView.as_view(), name='change_name'),
    path('myaccount/change_birthday', views.ChangeBirthdayView.as_view(), name='change_birthday'),
    path('myaccount/change_gender', views.ChangeGenderView.as_view(), name='change_gender'),
    path('myaccount/change_email', views.ChangeEmailView.as_view(), name='change_email'),
    path('myaccount/change_email/contact', views.ChangeRecoveryEmailView.as_view(), name='change_recovery_email'),
    path('myaccount/change_email/contact', views.ChangeContactEmailView.as_view(), name='change_contact_email'),
    path('myaccount/change_email/alternate', views.ChangeAlternateEmailView.as_view(), name='change_alternate_email'),

    path('myaccount/about_me', views.AddAboutView.as_view(), name='about_me'),
    # path('myaccount/about_me/work', views.UpdateWorkView.as_view(), name='update_work'),
    # path('myaccount/about_me/places', views.UpdatePlacesView.as_view(), name='update_places'),
    # path('myaccount/about_me/detail', views.UpdateDetailView.as_view(), name='update_detail'),

    path('profile/<slug:slug>', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:slug>/pdf/', views.download_cv_pdf, name="user-pdf"),
]
