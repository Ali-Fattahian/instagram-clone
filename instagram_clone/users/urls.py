from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('log-in/', views.LogInView.as_view(), name='log-in'),
    path('edit-profile/<slug:slug>',
         views.EditProfileView.as_view(), name='edit-profile'),
    path('search-results/',
         TemplateView.as_view(template_name='users/profile-list.html'), name='search-results'),
]
