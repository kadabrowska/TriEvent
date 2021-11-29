from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from TriEvent_app.models import PROFICIENCY, AGE_GROUP, DISTANCE, VOIVODESHIP, RATING


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=120, label='imię')
    last_name = forms.CharField(max_length=120, label="nazwisko")
    username = forms.CharField(max_length=120, label="login")
    email = forms.CharField(max_length=120, label='email', widget=forms.EmailInput, validators=[validate_email])
    password = forms.CharField(max_length=120, label="hasło", widget=forms.PasswordInput)
    proficiency = forms.ChoiceField(choices=PROFICIENCY, label="status")
    age_group = forms.ChoiceField(choices=AGE_GROUP, label='grupa wiekowa')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120, label='login', required=True)
    password = forms.CharField(max_length=120, label="hasło", widget=forms.PasswordInput, required=True)


class FindRaceForm(forms.Form):
    distance = forms.ChoiceField(choices=DISTANCE, label='dystans', required=False)
    voivodeship = forms.ChoiceField(choices=VOIVODESHIP, label='województwo', required=False)
    organiser = forms.CharField(max_length=255, label='organizator', required=False)


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=RATING)
    comment = forms.CharField(widget=forms.Textarea)



