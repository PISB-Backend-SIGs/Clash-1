from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import random

# Create your models here.
class Player(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    currentScore = models.IntegerField(blank=True,default=0)
    questionList =models.TextField(null=True,blank=True)
    questionNumber = models.IntegerField(default=random.randint(1,10),null=True,blank=True)  #random question number of player , current
    questionIndex = models.IntegerField(default=1)                                   #number visible to user sequentialy
    isStarted = models.BooleanField(default=False)              #to check user started quizz or not 
    isEnded = models.BooleanField(default=False)              #to check user started quizz or not 
    startTime = models.DateTimeField(null=True,blank=True)  #actual starting time
    endTime = models.DateTimeField(null=True,blank=True)  #game current time
    lifelineArray = models.TextField(blank=True,null=True,default="[]") #which lifelines are active 
    marksAdd = models.IntegerField(null=True,blank=True,default=4)  #marks add
    marksSubtract = models.IntegerField(null=True,blank=True,default=-2) #marks sub
    
    def __str__(self) -> str:
        return f"{self.user}"
    
class Lifeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lifelineID = models.IntegerField(default = 0)
    lifelineCounter = models.IntegerField(default=0,blank=True)
    isActive = models.BooleanField(default=False)


class Question(models.Model):
    questionID = models.IntegerField(unique=True,primary_key=True) #acc. to DB storage
    questionText = models.TextField()
    questionOption1 = models.TextField()
    questionOption2 = models.TextField()
    questionOption3 = models.TextField()
    questionOption4 = models.TextField()
    questionAnswer = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.q_id}"

class Submission(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    questionNumber = models.IntegerField()
    questionIndex = models.IntegerField(default=0) #player's ques index
    questionAnswer = models.IntegerField(null=True)
    score = models.IntegerField(null=True,blank=True)
    isLifelineActive = models.BooleanField(default=False) # for this question
    isCorrect = models.BooleanField(default= False) # is the subm. correct

    def __str__(self) -> str:
        return f"{self.player}"
    