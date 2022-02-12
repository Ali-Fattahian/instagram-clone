from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from .forms import SignUpForm, ProfileModelForm
from core.utils import OnlySameUserCanEditMixin
from verify_email.email_handler import send_verification_email


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'users/sign-up.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            send_verification_email(request, form)
            messages.info(request, 'Please verify your email, if you don\'t see anything, check the spam folder.')
            return redirect('users:sign-up')
        messages.error(request, 'Entered informations are not valid')
        return render(request, 'users/sign-up.html', context)


class LogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return redirect('core:homepage')
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('core:homepage')
        messages.error(request, 'Invalid information')
        return render(request, 'users/login.html')


def log_out(request):
    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('users:log-in')


class EditProfileView(OnlySameUserCanEditMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users/profile-edit.html'
    form_class = ProfileModelForm
    queryset = Profile.objects.all()

    def get_object(self):
        return get_object_or_404(Profile, slug=self.kwargs.get('slug'))


class ProfileListView(View):
    def get(self, request):
        return render(request, 'users/profile-list.html', {'profiles': Profile.objects.all().order_by('-date_joined')})

    def post(self, request):
        if request.POST.get('search_query'):
            search_query = request.POST.get('search_query')
            profiles = Profile.objects.filter(Q(username__icontains=search_query) | Q(
                first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        else:
            profiles = Profile.objects.all().order_by('-date_joined')
        return render(request, 'users/profile-list.html', {'profiles': profiles})


class ProfileDeleteConfirmationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile-delete-confirmation.html')

    def post(self, request):
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        user.is_active = False
        user.save()
        messages.info(request, 'Your account has been deleted, You can recover your account by sending your request with your account information to our email address.')
        return redirect('core:homepage')