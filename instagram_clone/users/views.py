from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from .forms import SignUpForm


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
        return render(request, 'users/sign-up.html', context)
