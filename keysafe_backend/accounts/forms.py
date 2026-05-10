from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'dob', 'email', 'security_question', 'security_answer']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class SecurityQuestionForm(forms.Form):
    answer = forms.CharField()


SECURITY_CHOICES = [
    ('school', 'What is your school name?'),
    ('player', 'Who is your favorite player?'),
    ('nickname', 'What is your nickname?'),
]

class UpdateSecurityQuestionForm(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '🔒 Current Password'
        })
    )

    security_question = forms.ChoiceField(
        choices=SECURITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    security_answer = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '🔐 New Security Answer'
        })
    )