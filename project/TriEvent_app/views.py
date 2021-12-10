from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from TriEvent_app.forms import RegistrationForm, LoginForm, FindRaceForm, EnrollForm
from TriEvent_app.models import Athlete, Race


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
        ctx = {'race': race}
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
            return redirect('registration', {"form": form})


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


class MyRacesView(View):
    """
    Shows races of the logged in athlete.
    """
    def get(self, request):
        return render(request, 'my_races.html')


class MyResultsView(View):
    """
    Shows results of the races the athlete was enrolled to.
    """
    def get(self, request):
        return render(request, 'my_results.html')


class MyProfileView(View):
    """
    Shows data of the athlete.
    """
    def get(self, request, user_id):
        athlete = User.objects.get(id=user_id)
        ctx = {'athlete': athlete}
        return render(request, 'profile.html', ctx)


class EnrollView(View):
    """
    Enroll button on the race-details page.
    It saves the race in the athlete's races.
    """
    def get(self, request, race_id):
        form = EnrollForm(initial={"athlete_id": request.user.id, "race_id": race_id})
        ctx = {'form': form}
        return render(request, 'race_details.html', ctx)

    def post(self, request, race_id):
        form = EnrollForm(request.POST)
        if form.is_valid():
            race_id = form.cleaned_data['race_id']
            athlete_id = form.cleaned_data['athlete_id']
            race = Race.objects.get(pk=race_id)
            athlete = Athlete.objects.get(pk=athlete_id)
            race.participants.add(athlete)
            ctx = {'form': form}
            return render(request, 'race_details.html', ctx)
        else:
            return render('race_details.html')













