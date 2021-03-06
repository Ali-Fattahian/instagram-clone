from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from .models import Post, LikePost, SavePost
from users.models import Follow, Profile
from .forms import CommentForm, LikePostForm, SavePostForm
# ------------------------------------------------------------


# Home Page View
class HomePageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_profile = request.user.profile
            newest_users = Profile.objects.all().order_by('-id')[:3] # For showing suggestions
            all_related_follow_objects = user_profile.followings.all()
            followed_users = []
            for follow_object in all_related_follow_objects:
                followed_users.append(follow_object.followed_user)
            posts = Post.objects.none()
            for followed_user in followed_users:
                posts = Post.objects.filter(profile=followed_user) | posts
            posts = posts | Post.objects.filter(profile=request.user.profile)
            user_liked_posts=[]
            for like_object in LikePost.objects.filter(profile=user_profile):
                if like_object.post in posts:
                    user_liked_posts.append(like_object.post)

            saved_posts = []
            for save_object in SavePost.objects.filter(profile=user_profile): # all the posts that user saved 
                # if save_object.post in posts:                     # if that post exist in posts that are shown to the user
                saved_posts.append(save_object.post) # add it to saved_posts list
            context = {'posts': posts.order_by(
                '-date_created'), 'comment_form': CommentForm(), 'like_post_form': LikePostForm(), 'save_post_form': SavePostForm, 'post_likes':user_liked_posts, 'suggested_users':newest_users, 'saved_posts':saved_posts}

            return render(request, 'core/homepage.html', context)
        posts = Post.objects.annotate(likes=Count('post_like')).order_by('-likes') #Show posts for non-auth users based on 'number of likes' or 'number of related LikePost objects to each post' order 

        return render(request, 'core/homepage.html', {'posts': posts})

    def post(self, request):
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            like_post_form = LikePostForm(request.POST)
            save_post_form = SavePostForm(request.POST)
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                post_id = request.POST['post_id']
                form.post = Post.objects.get(id=post_id)
                form.profile = request.user.profile
                form.save()
                return redirect('core:homepage')
            elif ( 'post_unsave_id' in request.POST or 'post_save_id' in request.POST): # if i use form validation here(before like_post_form validation) it won't work. Always the middle one doens't work normally.
                if request.POST.get('post_save_id'):
                    form = save_post_form.save(commit=False)
                    post_id = request.POST.get('post_save_id')
                    form.profile = request.user.profile
                    form.post = Post.objects.get(id=post_id)
                    form.save()
                elif request.POST.get('post_unsave_id'):
                    post_id = request.POST['post_unsave_id']
                    post = get_object_or_404(Post, pk=post_id)
                    save_object = SavePost.objects.get(post = post, profile = request.user.profile)
                    save_object.delete()
                return redirect('core:homepage')
            elif like_post_form.is_valid:
                if request.POST.get('like_post_id'):
                    form = like_post_form.save(commit=False)
                    post_id = request.POST['like_post_id']
                    form.profile = request.user.profile
                    form.post = Post.objects.get(id=post_id)
                    form.save()
                elif request.POST.get('dislike_post_id'):
                    post_id = request.POST['dislike_post_id']
                    post=Post.objects.get(pk=post_id)
                    like_object = LikePost.objects.get(profile=request.user.profile, post=post)
                    like_object.delete()
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
                return render(request, 'core/homepage.html', context)
        messages.error(request, 'You have to log in first!')
        return redirect('users:log-in')
## ------------------------------------------------------------


# User Profile Detail View
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
        if request.user.is_authenticated:
            profile = get_object_or_404(Profile, slug=slug)
            follow_request = request.POST.get('user-follow')
            unfollow_request = request.POST.get('user-unfollow')
            if follow_request:
                if Follow.objects.filter(followed_user=profile, following_user=request.user.profile).exists():
                    messages.error(request, 'You have already followed this user')
                    return redirect('core:user-account', slug=profile.slug)
                else:
                    Follow.objects.create(
                        followed_user=profile, following_user=request.user.profile)
                    messages.success(request, f'You are now following {profile.username}')
                    return redirect('core:user-account', slug=profile.slug)
            elif unfollow_request:
                follow_object = Follow.objects.filter(
                    followed_user=profile, following_user=request.user.profile)
                if follow_object.exists():
                    follow_object.delete()
                    messages.success(request, 'Unfollowed!')
                    return redirect('core:user-account', slug=profile.slug)
                else:
                    raise ValidationError('You didn\'t follow this user')
            raise ValidationError('You can either follow or unfollow a user')
        messages.error(request, 'You have to log in first!')
        return redirect('users:log-in')
# ------------------------------------------------------------


# Post Detail View
class PostDetailView(View):
    def get(self, request, slug, pk):
        post = get_object_or_404(Post, pk=pk)
        saved_posts = []
        if request.user.is_authenticated:
            save_objects = SavePost.objects.filter(profile = self.request.user.profile)
            for save_object in save_objects:
                saved_posts.append(save_object.post)
            is_post_like = LikePost.objects.filter(profile=request.user.profile, post = post)
        else:
            is_post_like = None
        context = {
            'post':post,
            'comment_form':CommentForm(),
            'like_post_form':LikePostForm(),
            'save_post_form': SavePostForm(),
            'is_post_like':is_post_like,
            'saved_posts': saved_posts
        }
        return render(request, 'core/post-detail.html', context)

    def post(self, request, slug, pk):
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            like_post_form = LikePostForm(request.POST)
            save_post_form = SavePostForm(request.POST)
            post = get_object_or_404(Post, pk=pk)
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                form.post = post
                form.profile = request.user.profile
                form.save()
                return HttpResponseRedirect(reverse('core:post', args=[slug, post.pk]))

            elif ( 'post_unsave' in request.POST or 'post_save' in request.POST): # Again i had to change the order of checking for post_save/unsave request and like/unlike request.
                if 'post_save' in request.POST:
                    form = save_post_form.save(commit=False)
                    form.profile = request.user.profile
                    form.post = post
                    form.save()
                    return HttpResponseRedirect(reverse('core:post', args=[slug, post.pk]))
                elif 'post_unsave' in request.POST:
                    saved_object = SavePost.objects.get(profile=self.request.user.profile, post=post)
                    saved_object.delete()
                    return HttpResponseRedirect(reverse('core:post', args=[slug, post.pk]))

            elif like_post_form.is_valid:
                is_post_like = LikePost.objects.filter(profile=request.user.profile, post = post)
                if is_post_like:
                    is_post_like.delete()
                    return HttpResponseRedirect(reverse('core:post', args=[slug, post.pk]))
                form = like_post_form.save(commit=False)
                form.post = post
                form.profile = request.user.profile
                form.save()
                return HttpResponseRedirect(reverse('core:post', args=[slug, post.pk]))
            else:
                context = {
                    'post': post,
                    'comment_form': comment_form,
                    'like_post_form': like_post_form
                }
                return render(request, 'core/post-detail.html', context)
        messages.error(request, 'You have to log in first!')
        return redirect('users:log-in')
# ------------------------------------------------------------


# Add Post View
class AddPostView(LoginRequiredMixin, View):
    login_url = 'users:log-in'
    redirect_field_name = 'next' # this next functionality working for this view because of this

    def get(self, request):
        return render(request, 'core/new-post.html')

    def post(self, request):
        post_content = request.POST.get('post-caption')
        post_image = request.FILES.get('post-image')
        post_profile = request.user.profile
        post = Post(profile=post_profile, content=post_content, image=post_image)
        try:
            post.full_clean()
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('core:user-account', slug=post_profile.slug)
        except ValidationError:
            messages.error(request, 'There was a problem creating the post, Make sure everything is correct!')
            return render(request, 'core/new-post.html')
# ------------------------------------------------------------


# Explore Page View
def explore(request):
    posts = Post.objects.all().order_by('-date_created')
    context = {'posts':posts}
    return render(request, 'core/explore.html', context)
# ------------------------------------------------------------


# Coming Soon Page
def coming_soon(request):
    return render(request, 'coming-soon.html')
# ------------------------------------------------------------    


# Saved Post View
class SavedPostsView(LoginRequiredMixin, ListView):
    template_name = 'core/saved-posts.html'
    context_object_name = 'saved_posts'

    def get_queryset(self):
        return SavePost.objects.filter(profile=self.request.user.profile)
# ------------------------------------------------------------        
    

# Delete Post View
class DeletePostView(LoginRequiredMixin ,View):
    def get(self, request):
        profile = request.user.profile
        posts = Post.objects.filter(profile=profile)
        return render(request, 'core/delete-post.html', {'posts':posts})

    def post(self, request):
        post_id = request.POST.get('post-delete-id')
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return redirect('core:delete-post')
