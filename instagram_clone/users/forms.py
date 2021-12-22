from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1',
                  'password2', 'first_name', 'last_name')
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), strip=False)
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password confirmation'}), strip=False)

        widgets = {
            'username': forms.fields.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.fields.TextInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.fields.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.fields.TextInput(attrs={'placeholder': 'Last name'}),
            'password1':forms.fields.TextInput(attrs={'placeholder':'Password'})
        }
