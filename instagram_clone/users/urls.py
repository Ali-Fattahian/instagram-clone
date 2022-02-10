from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('log-in/', views.LogInView.as_view(), name='log-in'),
    path('log-out/', views.log_out, name='log-out'),
    path('edit-profile/<slug:slug>',
         views.EditProfileView.as_view(), name='edit-profile'),
    path('profile-delete/', views.ProfileDeleteConfirmationView.as_view(), name='profile-delete'),
    path('search-results/', views.ProfileListView.as_view(), name='search-results'),
]
