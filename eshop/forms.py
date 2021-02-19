from django import forms
from .models import User

class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'email','password','phone','address')
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput() }