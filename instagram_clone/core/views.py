from django.shortcuts import render
from django.views.generic import View
from .models import Post


class HomePageView(View):
    def get(self, request):
        user_profile = request.user.profile
        all_related_follow_objects = user_profile.followings.all()
        followed_users = []
        for follow_object in all_related_follow_objects:
            followed_users.append(follow_object.followed_user)
        posts = Post.objects.none()
        for followed_user in followed_users:
            posts = Post.objects.filter(profile=followed_user) | posts

        context = {'posts': posts.order_by('-date_created')}
        return render(request, 'core/homepage.html', context)

    def post(self, request):
        pass
