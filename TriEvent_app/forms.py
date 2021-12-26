from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from psycopg2 import extras

from TriEvent_app.models import PROFICIENCY, AGE_GROUP, DISTANCE, VOIVODESHIP


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=120, label='imię')
    last_name = forms.CharField(max_length=120, label="nazwisko")
    username = forms.CharField(max_length=120, label="login")
    email = forms.CharField(max_length=120, label='email',
                            widget=forms.EmailInput,
                            validators=[validate_email])
    password = forms.CharField(max_length=120, label="hasło",
                               widget=forms.PasswordInput)
    proficiency = forms.ChoiceField(choices=PROFICIENCY, label="status")
    age_group = forms.ChoiceField(choices=AGE_GROUP, label='grupa wiekowa')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120, label='login',required=True)
    password = forms.CharField(max_length=120, label="hasło", widget=forms.PasswordInput,
                               required=True)


class FindRaceForm(forms.Form):
    distance = forms.ChoiceField(choices=DISTANCE, label='dystans', required=False)
    voivodeship = forms.ChoiceField(choices=VOIVODESHIP, label='województwo', required=False)
    organiser = forms.CharField(max_length=255, label='organizator', required=False)


class EnrollForm(forms.Form):
    athlete_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    race_id = forms.IntegerField(widget=forms.HiddenInput, required=False)


# def validate_format():
#     if format() != '%H:%M:%S':
#         raise ValidationError("Czas podaj w formacie HH:MM:SS")


class AddResultsForm(forms.Form):
    race = forms.IntegerField(widget=forms.HiddenInput, required=False)
    athlete = forms.IntegerField(widget=forms.HiddenInput, required=False)
    swim = forms.TimeField(label='pływanie', required=True, widget=forms.TimeInput(format='%H:%M:%S'))
    T1 = forms.TimeField(label='T1', required=True, widget=forms.TimeInput(format='%H:%M:%S'))
    bike = forms.TimeField(label='rower', required=True, widget=forms.TimeInput(format='%H:%M:%S'))
    T2 = forms.TimeField(label='T2', required=True, widget=forms.TimeInput(format='%H:%M:%S'))
    run = forms.TimeField(label='bieg', required=True, widget=forms.TimeInput(format='%H:%M:%S'))


class AddRaceForm(forms.Form):
    name = forms.CharField(label='nazwa zawodów', max_length=255)
    organiser = forms.CharField(label='organizator', max_length=255)
    distance = forms.ChoiceField(label='dystans', choices=DISTANCE)
    date = forms.DateField(label='data')
    city = forms.CharField(label='miasto', max_length=255)
    voivodeship = forms.ChoiceField(label='województwo', choices=VOIVODESHIP)
    description = forms.CharField(label='opis', widget=forms.Textarea)
    race_url = forms.URLField(label='link do zapisów')


 # class ReviewForm(forms.Form):
 #     race = forms.IntegerField(widget=forms.HiddenInput, required=False)
 #     rating = forms.ChoiceField(choices=RATING, label='Ocena:')
 #     comment = forms.CharField(widget=forms.Textarea, label="Napisz coś...")


# class ResetProfileForm(forms.Form):
#     password = forms.CharField(max_length=120, label="nowe hasło",
#                               widget=forms.PasswordInput, required=True)
#     proficiency = forms.ChoiceField(choices=PROFICIENCY, label="nowy status",
#                                    required=True)
#     age_group = forms.ChoiceField(choices=AGE_GROUP, label='nowa grupa wiekowa',
#                                   required=True)


