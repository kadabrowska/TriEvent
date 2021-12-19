from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from TriEvent_app.forms import RegistrationForm, LoginForm, FindRaceForm, EnrollForm, AddResultsForm
from TriEvent_app.models import Athlete, Race, Results


class HomepageView(View):
    """
    Homepage view.
    """
    def get(self, request):
        return render(request, "base.html")


class FindRaceView(View):
    """
    Searching for races by distance, organiser and voivodeship.
    """
    def get(self, request):
        form = FindRaceForm()
        ctx = {'form': form}
        return render(request, "find_race.html", ctx)


class RacesListView(View):
    """
    List of the races that meet the searching requirements.
    If there are no races, the user gets information about it.
    """
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

        ctx = {'races_list': races_list}
        return render(request, "races_list.html", ctx)


class RaceDetailsView(View):
    """
    Details of the chosen race, such as name, date, description, url.
    """
    def get(self, request, race_id):
        race = Race.objects.get(id=race_id)
        athletes = race.participants.all()
        ctx = {'race': race, 'athletes': athletes}
        return render(request, "race_details.html", ctx)


class RegistrationView(View):
    """
    User registration page. Email address cannot be duplicated.
    After registration it redirects to registration success page.
    """
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
                form.add_error('email',
                               "Konto z tym adresem email już istnieje")

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

        else:
            return redirect('registration')


class LoginView(View):
    """
    Login form with username and password. It redirects to find-races afterwards.
    """
    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
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
        ctx = {'form': form}
        return render(request, "login.html", ctx)


class RegistrationSuccessfulView(View):
    """
    Success page after registration.
    """
    def get(self, request):
        return render(request, "registration_successful.html")


class LogoutView(View):
    """
    Logout option.
    """
    def get(self, request):
        logout(request)
        return redirect("login")


class MyRacesView(LoginRequiredMixin, View):
    """
    Shows races of the logged in athlete.
    """
    def get(self, request):
        user = request.user.id
        athlete = Athlete.objects.filter(user_id=user)
        races = Race.objects.filter(participants=athlete)
        ctx = {'races': races}
        return render(request, 'my_races.html', ctx)


class DeleteMyRaceView(View):
    """
    Deleting races from the list.
    """
    def get(self, request, race_id):
        user = request.user.id
        athlete = Athlete.objects.filter(user_id=user)
        race = Race.objects.get(pk=race_id)
        race.participants.remove(athlete)
        return redirect('my-races')


class AddResultsView(LoginRequiredMixin, View):
    """
    Adding  results to a particular race.
    """
    def get(self, request, race_id):
        race = Race.objects.get(id=race_id)
        user = request.user.id
        athlete = Athlete.objects.filter(user_id=user)
        form = AddResultsForm()
        ctx = {'form': form, 'race': race, 'athlete': athlete}
        return render(request, 'add_results.html', ctx)

    def post(self, request, race_id):
        form = AddResultsForm(request.POST)
        if form.is_valid():
            swim = form.cleaned_data['swim']
            T1 = form.cleaned_data['T1']
            bike = form.cleaned_data['bike']
            T2 = form.cleaned_data['T2']
            run = form.cleaned_data['run']
            race = Race.objects.get(pk=race_id)
            user = request.user.id
            athlete = Athlete.objects.filter(user_id=user)
            if not Results.objects.filter(race=race, athlete=athlete).exists():
                Results.objects.create(
                    race=race,
                    athlete=athlete,
                    swim=swim,
                    T1=T1,
                    bike=bike,
                    T2=T2,
                    run=run,
                )
            else:
                Results.objects.update(
                    race=race,
                    athlete=athlete,
                    swim=swim,
                    T1=T1,
                    bike=bike,
                    T2=T2,
                    run=run,
                )
            return redirect('my-results')
        else:
            return render(request, 'add_results.html')


class DeleteResultsView(View):
    """
    Deletes the results of a particular race
    """
    def get(self, results_id):
        results = Results.objects.get(pk=results_id)
        results.delete()
        return redirect('/my/results/')


class MyResultsView(LoginRequiredMixin, View):
    """
    Shows results of the races the athlete was enrolled to.
    Only for authenticated users.
    """
    def get(self, request):
        user = request.user.id
        athlete = Athlete.objects.filter(user_id=user)
        results = Results.objects.filter(athlete=athlete)
        ctx = {'results': results}
        return render(request, 'my-results', ctx)


class MyProfileView(LoginRequiredMixin, View):
    """
    Shows data of the athlete.
    Only for authenticated users.
    """
    def get(self, request, user_id):
        athlete = User.objects.get(id=user_id)
        ctx = {'athlete': athlete}
        return render(request, 'profile.html', ctx)


class EnrollView(LoginRequiredMixin, View):
    """
    Enroll button on the race-details page.
    It saves the race in the athlete's races.
    Only for authenticated users.
    """
    def get(self, request, race_id, user_id):
        form = EnrollForm(initial={"athlete_id": user_id, "race_id": race_id})
        ctx = {'form': form}
        return render(request, 'race_details.html', ctx)

    def post(self, request, race_id, user_id):
        race = Race.objects.get(pk=race_id)
        athlete = Athlete.objects.get(user_id=user_id)
        form = EnrollForm(request.POST)
        if form.is_valid():
            race.participants.add(athlete)
            ctx = {'form': form, 'race': race}
            return render(request, 'enroll.html', ctx)
        else:
            return render(request, 'race_details.html')
