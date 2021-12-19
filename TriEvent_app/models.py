from django.contrib.auth.models import User
from django.db import models
from datetime import date


DISTANCE = (
    ("Super Sprint", "Super Sprint"),
    ("Sprint", "Sprint"),
    ("Olimpijski", "Olimpijski"),
    ("1/4", "1/4"),
    ("1/2", "1/2"),
    ("Ironman", "Ironman"),
)

VOIVODESHIP = (
    ("dolnośląskie", "dolnośląskie"),
    ("kujawsko-pomorskie", "kujawsko-pomorskie"),
    ("lubelskie", "lubelskie"),
    ("lubuskie", "lubuskie"),
    ("łódzkie", "łódzkie"),
    ("małopolskie", "małopolskie"),
    ("mazowieckie", "mazowieckie"),
    ("opolskie", "opolskie"),
    ("podkarpackie", "podkarpackie"),
    ("podlaskie", "podlaskie"),
    ("pomorskie", "pomorskie"),
    ("śląskie", "śląskie"),
    ("świętokrzyskie", "świętokrzyskie"),
    ("warmińsko-mazurskie", "warmińsko-mazurskie"),
    ("wielkopolskie", "wielkopolskie"),
    ("zachodniopomorskie", "zachodniopomorskie"),
)

AGE_GROUP = (
    ("UNDER-19", "UNDER-19"),
    ("20-24", "20-24"),
    ("25-29", "25-29"),
    ("30-34", "30-34"),
    ("35-39", "35-39"),
    ("40-44", "40-44"),
    ("45-49", "45-49"),
    ("50-54", "50-54"),
    ("55-59", "55-59"),
    ("60-64", "60-64"),
    ("65-OVER", "65-OVER"),
)

PROFICIENCY = (
    ("amateur", "amateur"),
    ("professional", "professional"),
)

RATING = (
    ("słabo", "słabo"),
    ("tak sobie", "tak sobie"),
    ("OK", "OK"),
    ("fajnie", "fajnie"),
    ("rewelacja", "rewelacja"),
)


class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    proficiency = models.CharField(choices=PROFICIENCY, max_length=30, default=None)
    age_group = models.CharField(choices=AGE_GROUP, max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)


class Race(models.Model):
    name = models.CharField(max_length=255)
    organiser = models.CharField(max_length=255)
    distance = models.IntegerField(choices=DISTANCE)
    date = models.DateField(default=date.today)
    city = models.CharField(max_length=255)
    voivodeship = models.CharField(choices=VOIVODESHIP, max_length=50)
    description = models.CharField(max_length=1500)
    race_url = models.URLField()
    participants = models.ManyToManyField(Athlete)


class Results(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    swim = models.TimeField()
    T1 = models.TimeField()
    bike = models.TimeField()
    T2 = models.TimeField()
    run = models.TimeField()


class Review(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default='Anonim')
    rating = models.IntegerField(choices=RATING)
    comment = models.TextField(max_length=500)
