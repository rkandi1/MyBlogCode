from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=30, label="email")
    password = forms.PasswordInput()