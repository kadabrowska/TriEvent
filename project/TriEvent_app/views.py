from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

from TriEvent_app.forms import RegistrationForm
from TriEvent_app.models import Athlete
from django.views.generic import CreateView, DetailView


class HomepageView(View):
    def get(self, request):
        return render(request, "base.html")


class FindRaceView(View):
    def get(self, request):
        return render(request, "find_race.html")


class RacesListView(View):
    def get(self, request):
        return render(request, "races_list.html")


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
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            proficiency = form.cleaned_data["proficiency"]
            age_group = form.cleaned_data["age_group"]

            if Athlete.objects.filter(email=email):
                form.add_error('email', "Konto z tym adresem email już istnieje")

            if not form.errors:
                athlete = Athlete.objects.create(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    proficiency=proficiency,
                    age_group=age_group
                )
                login(request, athlete)
                return redirect('find-race')

            ctx = {"form": form}
            return render(request, "registration_page.html", ctx)

