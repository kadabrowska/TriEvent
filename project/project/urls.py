"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from TriEvent_app.views import HomepageView, FindRaceView, RacesListView, RegistrationView, LoginView, \
    RegistrationSuccessfulView, RaceDetailsView, LogoutView, MyRacesView, MyResultsView, MyProfileView, EnrollView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name="homepage"),
    path('findrace/', FindRaceView.as_view(), name="find-race"),
    path('races/', RacesListView.as_view(), name="races-list"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('registration/successful/', RegistrationSuccessfulView.as_view(), name="registration-successful"),
    path('login/', LoginView.as_view(), name='login'),
    path('races/details/<int:race_id>/', RaceDetailsView.as_view(), name='race-details'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my/races/', MyRacesView.as_view(), name='my-races'),
    path('my/results/', MyResultsView.as_view(), name='my-results'),
    path('my/profile/<int:user_id>/', MyProfileView.as_view(), name='my-profile'),
    path('races/details/<int:race_id>/enroll/<int:user_id>', EnrollView.as_view(), name='enroll-athlete'),
]
