from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.HomePageView.as_view(), name='homepage'),
    path('homepage/explore', views.explore, name='explore'),
    path('homepage/add-post', views.AddPostView.as_view(), name='add-post'),
    path('homepage/<slug:slug>',
         views.UserProfileDetail.as_view(), name='user-account'),
    path('saved-posts/', views.SavedPostsView.as_view(), name='saved-posts'), #It can cause some problem because django expects a slug after homepage, and saved-posts looks like it.
    path('homepage/<slug:slug>/posts/<int:pk>/',
         views.PostDetailView.as_view(), name='post'),
    path('chat/', views.coming_soon, name='coming-soon')
]
