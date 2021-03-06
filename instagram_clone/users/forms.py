from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile


class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1',
                  'password2', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Password Confirmation'})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last Name'})

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower()
        return email


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'first_name',
                  'last_name', 'username', 'bio', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower()
        return email
