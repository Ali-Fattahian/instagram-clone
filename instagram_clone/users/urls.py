from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('log-in/', views.LogInView.as_view(), name='log-in'),
    path('edit-profile/<slug:slug>',
         views.EditProfileView.as_view(), name='edit-profile'),
]
