from django import forms
from django.core.validators import validate_email

from TriEvent_app.models import PROFICIENCY, AGE_GROUP


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=120, label='imię')
    last_name = forms.CharField(max_length=120, label="nazwisko")
    email = forms.CharField(max_length=120, label='email', widget=forms.EmailInput, validators=[validate_email])
    password = forms.CharField(max_length=120, label="hasło", widget=forms.PasswordInput)
    proficiency = forms.ChoiceField(choices=PROFICIENCY, label="status")
    age_group = forms.ChoiceField(choices=AGE_GROUP, label='grupa wiekowa')



