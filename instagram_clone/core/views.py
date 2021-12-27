from django.shortcuts import redirect, render
from django.views.generic import View, DetailView
from .models import Post
from users.models import Follow, Profile
from .forms import CommentForm


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

        context = {'posts': posts.order_by('-date_created'), 'comment_form':CommentForm()}
        return render(request, 'core/homepage.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                post_id = request.POST['post_id']
                form.post = Post.objects.get(id=post_id)
                form.profile = request.user.profile
                form.save()
                print('comment added')
                return redirect('core:homepage')
            else:
                user_profile = request.user.profile
                all_related_follow_objects = user_profile.followings.all()
                followed_users = []
                for follow_object in all_related_follow_objects:
                    followed_users.append(follow_object.followed_user)
                posts = Post.objects.none()
                for followed_user in followed_users:
                    posts = Post.objects.filter(profile=followed_user) | posts

                context = {'posts': posts.order_by('-date_created'), 'comment_form':comment_form}
                print('show comment errors')
                return render(request, 'core/homepage.html', context)
        print('log in first!')
        return redirect('core:homepage')


class UserProfileDetail(DetailView):
    model = Profile
    template_name = 'core/user-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        followers = Follow.objects.filter(followed_user=profile)
        followings = Follow.objects.filter(following_user=profile)
        if self.request.user.is_authenticated: #Little help for guests
            is_follower = Follow.objects.filter(followed_user=profile, following_user=self.request.user.profile)
            context['request_user_is_follower']=is_follower #checks if the person visiting is following that user or not
        context['posts'] = Post.objects.filter(profile=self.object)
        context['followers'] = followers
        context['followings'] = followings
        return context

    context_object_name = 'profile'