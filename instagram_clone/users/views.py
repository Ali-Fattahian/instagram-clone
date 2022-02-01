from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from .models import Profile
from .forms import SignUpForm
from core.utils import OnlySameUserCanEditMixin


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'users/sign-up.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('users:sign-up')
        print('Entered informations are not valid')
        return render(request, 'users/sign-up.html', context)


class LogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            print('You are already logged in')
            return redirect('core:homepage')
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:homepage')
        print('Invalid information')
        return render(request, 'users/login.html')


class EditProfileView(OnlySameUserCanEditMixin, UpdateView):
    model = Profile
    fields = ('image', 'first_name', 'last_name', 'username', 'bio', 'email')
    template_name = 'users/profile-edit.html'


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
