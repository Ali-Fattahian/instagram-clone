from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('explore', views.explore, name='explore'),
    path('posts/add-post', views.AddPostView.as_view(), name='add-post'),
    path('<slug:slug>',
         views.UserProfileDetail.as_view(), name='user-account'),
    # It can cause some problem because django expects a slug after homepage, and saved-posts looks like it.
    path('posts/saved-posts/', views.SavedPostsView.as_view(), name='saved-posts'),
    path('<slug:slug>/posts/<int:pk>/',
         views.PostDetailView.as_view(), name='post'),
    path('posts/delete', views.DeletePostView.as_view(), name='delete-post'),
    path('chat/', views.coming_soon, name='coming-soon')
]
