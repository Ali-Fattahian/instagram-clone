from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.HomePageView.as_view(), name='homepage'),
    path('homepage/<slug:slug>',
         views.UserProfileDetail.as_view(), name='user-account'),
    path('homepage/<slug:slug>/posts/<int:pk>/',
         views.PostDetailView.as_view(), name='post'),
]
