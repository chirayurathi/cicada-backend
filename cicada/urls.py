"""cicada URL Configuration

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
from quizapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/',test),
    path('login/',login),
    path('teams/register/',registerTeam),
    path('teams/detail/<int:id>/',getTeam),
    path('teams/update/<int:id>/',updateTeam),
    path('teams/delete/<int:id>/',deleteTeam),
    path('teams/detail/',getAllTeams),
    path('players/add/',addPlayer),
    path('players/detail/<int:id>',getPlayer),
    path('players/update/<int:id>/',updatePlayer),
    path('players/delete/<int:id>/',deletePlayer),
    path('tracks/add/',addTrack),
    path('tracks/detail/<int:id>',getTrack),
    path('tracks/update/<int:id>/',updateTrack),
    path('tracks/delete/<int:id>/',deleteTrack),
    path('tracks/detail/',getAllTracks),
    path('questions/add/',addQuestion),
    path('questions/detail/<int:id>/',getQuestion),
    path('questions/update/<int:id>/',updateQuestion),
    path('questions/delete/<int:id>/',deleteQuestion),
]
