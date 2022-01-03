from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ValidationError
from django.views.generic import View
from .models import Post, LikePost
from users.models import Follow, Profile
from .forms import CommentForm, LikePostForm


class HomePageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_profile = request.user.profile
            all_related_follow_objects = user_profile.followings.all()
            followed_users = []
            for follow_object in all_related_follow_objects:
                followed_users.append(follow_object.followed_user)
            posts = Post.objects.none()
            for followed_user in followed_users:
                posts = Post.objects.filter(profile=followed_user) | posts
            user_liked_posts=[]
            for like_object in LikePost.objects.filter(profile=user_profile):
                if like_object.post in posts:
                    user_liked_posts.append(like_object.post)

            context = {'posts': posts.order_by(
                '-date_created'), 'comment_form': CommentForm(), 'like_post_form': LikePostForm(), 'post_likes':user_liked_posts}

            return render(request, 'core/homepage.html', context)
        posts = Post.objects.all()
        return render(request, 'core/homepage.html', {'posts': posts})

    def post(self, request):
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            like_post_form = LikePostForm(request.POST)
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                post_id = request.POST['post_id']
                form.post = Post.objects.get(id=post_id)
                form.profile = request.user.profile
                form.save()
                print('comment added')
                return redirect('core:homepage')
            elif like_post_form.is_valid:
                form = like_post_form.save(commit=False)
                post_id = request.POST['like_post_id']
                form.profile = request.user.profile
                form.post = Post.objects.get(id=post_id)
                form.save()
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

                context = {'posts': posts.order_by(
                    '-date_created'), 'comment_form': comment_form}
                print('show comment errors')
                return render(request, 'core/homepage.html', context)
        print('log in first!')
        return redirect('core:homepage')


class UserProfileDetail(View):
    def get(self, request, slug):
        profile = get_object_or_404(Profile, slug=slug)
        context = dict()
        followers = Follow.objects.filter(followed_user=profile)
        followings = Follow.objects.filter(following_user=profile)
        if self.request.user.is_authenticated:  # Little help for guests
            is_follower = Follow.objects.filter(
                followed_user=profile, following_user=self.request.user.profile)
            # checks if the person visiting is following that user or not
            context['request_user_is_follower'] = is_follower
        context['posts'] = Post.objects.filter(profile=profile)
        context['followers'] = followers
        context['followings'] = followings
        context['profile'] = profile

        return render(request, 'core/user-account.html', context)

    def post(self, request, slug):
        profile = get_object_or_404(Profile, slug=slug)
        follow_request = request.POST.get('user-follow')
        unfollow_request = request.POST.get('user-unfollow')
        if follow_request:
            if Follow.objects.filter(followed_user=profile, following_user=request.user.profile).exists():
                # print('you have already followed this user')
                return redirect('core:user-account', slug=profile.slug)
            else:
                Follow.objects.create(
                    followed_user=profile, following_user=request.user.profile)
                print('follow accepted')
                return redirect('core:user-account', slug=profile.slug)
        elif unfollow_request:
            follow_object = Follow.objects.filter(
                followed_user=profile, following_user=request.user.profile)
            if follow_object.exists():
                follow_object.delete()
                # print('successfully unfollowed')
                return redirect('core:user-account', slug=profile.slug)
            else:
                raise ValidationError('You didn\'t follow this user')
        raise ValidationError('You can either follow or unfollow a user')


class PostDetailView(View):
    def get(self, request, slug, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {
            'post':post,
            'comment_form':CommentForm(),
            'like_post_form':LikePostForm(),
        }
        return render(request, 'core/post-detail.html', context)

    def post(self, request, pk):
        pass