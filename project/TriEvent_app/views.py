from datetime import timedelta, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views import View

from TriEvent_app.forms import RegistrationForm, LoginForm, FindRaceForm
from TriEvent_app.models import Athlete, Race, PROFICIENCY, AGE_GROUP
from django.views.generic import CreateView, DetailView


class HomepageView(View):
    def get(self, request):
        return render(request, "base.html")


class FindRaceView(View):
    def get(self, request):
        form = FindRaceForm()
        ctx = {'form': form}
        return render(request, "find_race.html", ctx)


class RacesListView(View):
    def get(self, request):
        distance = request.GET.get('distance')
        voivodeship = request.GET.get('voivodeship')
        organiser = request.GET.get('organiser')

        races_list = Race.objects.all()
        if distance:
            races_list = races_list.filter(distance=distance)
        if voivodeship:
            races_list = races_list.filter(voivodeship=voivodeship)
        if organiser:
            races_list = races_list.filter(organiser=organiser)

        ctx = {
            'races_list':races_list
        }
        return render(request, "races_list.html", ctx)


class RaceDetailsView(View):
    def get(self, request, race_id):
        race = Race.objects.get(id=race_id)
        ctx = {'race':race}
        return render(request, "race_details.html", ctx)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        ctx = {'form': form}
        return render(request, "registration_page.html", ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            proficiency = form.cleaned_data["proficiency"]
            age_group = form.cleaned_data["age_group"]

            if User.objects.filter(email=email):
                form.add_error('email', "Konto z tym adresem email już istnieje")

            if not form.errors:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    username=username,
                )
                Athlete.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    proficiency=proficiency,
                    age_group=age_group,)
                login(request, user)
                return redirect('registration-successful')

            ctx = {"form": form}
            return render(request, "registration_page.html", ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'form':form}
        return render(request, "login.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            athlete = authenticate(username=username, password=password)
            if athlete is not None:
                login(request, athlete)
                return redirect('{}?login=True'.format(reverse('find-race')))
            else:
                form.add_error(None, "Niepoprawny email i/lub hasło")
        ctx = {'form':form}
        return render(request, "login.html", ctx)


class RegistrationSuccessfulView(View):
    def get(self, request):
        return render(request, "registration_successful.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class MyRacesView(View):
    def get(self, request):
        return render(request, 'my_races.html')


class MyResultsView(View):
    def get(self, request):
        return render(request, 'my_results.html')


class MyProfileView(View):
    def get(self, request):
        athlete = Athlete.objects.all()
        ctx = {'athlete': athlete}
        return render(request, 'profile.html', ctx)









