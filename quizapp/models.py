from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey
from rest_framework.authentication import TokenAuthentication

class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    
class Track(models.Model):
    track_name = models.CharField(max_length=30, null=True, blank=True)

class Team(AbstractUser):
    track = models.ForeignKey(to=Track,null=True, blank=True, related_name='team', on_delete=models.SET_NULL)
    score = models.IntegerField(default=0)

class Player(models.Model):
    team = models.ForeignKey(to=Team, related_name='player', on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(unique=True)

class Question(models.Model):
    track = ForeignKey(to=Track, related_name='question', on_delete=models.CASCADE)
    question_no = models.IntegerField()
    question = models.TextField(max_length=300)
    correct_answer = models.CharField(max_length=100)

class Answer(models.Model):
    question = models.ForeignKey(to=Question, related_name='answer', on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, related_name='answer', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField()