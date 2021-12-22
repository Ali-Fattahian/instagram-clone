from django.views.generic.edit import FormView
from .forms import SignUpForm


class SignUpView(FormView):
    template_name = 'users/sign-up.html'
    form_class = SignUpForm
    success_url = '/users/sign-up.html/'
