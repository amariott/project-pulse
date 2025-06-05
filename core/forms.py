from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your username',
        'class': "w-full py-4 px-6 rounded-xl"
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your email',
        'class': "w-full py-4 px-6 rounded-xl"
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'your password',
        'class': "w-full py-4 px-6 rounded-xl"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'repeat password',
        'class': "w-full py-4 px-6 rounded-xl"
    }))


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your username',
        'class': "w-full py-4 px-6 rounded-xl"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'your password',
        'class': "w-full py-4 px-6 rounded-xl"
    }))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'age', 'card_number', 'address')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
            'age': forms.NumberInput(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
            'card_number': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
            'address': forms.Textarea(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'rows': 3}),
        }