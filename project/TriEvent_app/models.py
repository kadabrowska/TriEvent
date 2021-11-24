from django.db import models


DISTANCE = (
    (1, "Super Sprint"),
    (2, "Sprint"),
    (3, "Olimpijski"),
    (4, "1/4"),
    (5, "1/2"),
    (6, "Ironman"),
)

VOIVODESHIP = (
    (1, "dolnośląskie"),
    (2, "kujawsko-pomorskie"),
    (3, "lubelskie"),
    (4, "lubuskie"),
    (5, "łódzkie"),
    (6, "małopolskie"),
    (7, "mazowieckie"),
    (8, "opolskie"),
    (9, "podkarpackie"),
    (10, "podlaskie"),
    (11, "pomorskie"),
    (12, "śląskie"),
    (13, "świętokrzyskie"),
    (14, "warmińsko-mazurskie"),
    (15, "wielkopolskie"),
    (16, "zachodniopomorskie"),
)

AGE_GROUP = (
    (1, "UNDER-19"),
    (2, "20-24"),
    (3, "25-29"),
    (4, "30-34"),
    (5, "35-39"),
    (6, "40-44"),
    (7, "45-49"),
    (8, "50-54"),
    (9, "55-59"),
    (10, "60-64"),
    (11, "65-OVER"),
)

PROFICIENCY = (
    (1, "amateur"),
    (2, "professional"),
)

RATING = (
    (1, "słabo"),
    (2, "tak sobie"),
    (3, "OK"),
    (4, "fajnie"),
    (5, "rewelacja"),
)


class Athlete(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=60)
    proficiency = models.CharField(choices=PROFICIENCY, max_length=30, default=None)
    age_group = models.CharField(choices=AGE_GROUP, max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)


class Race(models.Model):
    name = models.CharField(max_length=255)
    organiser = models.CharField(max_length=255)
    distance = models.IntegerField(choices=DISTANCE)
    city = models.CharField(max_length=255)
    voivodeship = models.CharField(choices=VOIVODESHIP, max_length=50)
    description = models.CharField(max_length=1500)
    race_url = models.URLField()
    participants = models.ManyToManyField(Athlete)


class Results(models.Model):
    race_name = models.ForeignKey(Race, on_delete=models.CASCADE)
    player_name = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    swim = models.TimeField()
    T1 = models.TimeField()
    bike = models.TimeField()
    T2 = models.TimeField()
    run = models.TimeField()


class Review(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING)
    comment = models.TextField(max_length=500)


