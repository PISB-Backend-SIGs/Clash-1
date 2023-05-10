from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import random 

# Create your models here.
class Player(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    playerScore = models.IntegerField(blank=True,default=0)
    questionList=models.TextField(null=True,blank=True)
    questionNumber = models.IntegerField(default=random.randint(1,10),null=True,blank=True)  #random question number of player
    questionIndex = models.IntegerField(default=1)                                   #number visible to user sequentialy
    isStarted=models.BooleanField(default=False)              #to check user started quizz or not 
    isEnded=models.BooleanField(default=False)              #to check user started quizz or not 
    rank = models.IntegerField(blank=True,null=True)
    previousQuestion = models.IntegerField(blank=True,default=0)
    startTime = models.DateTimeField(null=True,blank=True)  #actual starting time
    EndTime = models.DateTimeField(null=True,blank=True)  #game current time
    lifelineArray = models.TextField(blank=True,null=True,default="[]")
    lifelineActivationFlag = models.BooleanField(default=False)
    marksAdd=models.IntegerField(null=True,blank=True,default=4)  #marks add
    marksSubstract=models.IntegerField(null=True,blank=True,default=-2) #marks sub
    chatBotResponse = models.TextField(blank = True) # store chatBot ques. and ans 3rd lifelinr
    isTeamChoices = [
        (True,"True"),
        (False,"False")
    ]
    isTeam = models.BooleanField(choices=isTeamChoices,default=True)
    isJuniorChoices = [
        (True,"True"),
        (False,"False")
    ]
    isJunior = models.BooleanField(choices=isJuniorChoices,default=True)
    tabSwitchCount = models.IntegerField(default=0)
    maxStreak = models.IntegerField(default = 0)


    def __str__(self) -> str:
        return f"{self.user}"
    
# if multiple lifeline 
class Lifeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lifelineID = models.IntegerField(default = 0)
    lifelineCounter = models.IntegerField(default=0,blank=True)
    isActive = models.BooleanField(default=False)


class Question(models.Model):
    questionID = models.IntegerField(unique=True,primary_key=True)
    questionNumber = models.IntegerField(null=True)
    questionText = models.TextField()
    questionOption1 = models.TextField()
    questionOption2 = models.TextField()
    questionOption3 = models.TextField()
    questionOption4 = models.TextField()
    questionAnswer = models.IntegerField()
    forJunior = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f"{self.questionID}"

class Submission(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    questionID = models.IntegerField()
    questionIndex = models.IntegerField(default=0) #player's ques index
    userOption = models.IntegerField(null=True)
    points = models.IntegerField(null=True,blank=True)
    lifelineActivated = models.BooleanField(default=False)
    isCorrect = models.BooleanField(default= False)

    def __str__(self) -> str:
        return f"{self.player}"
    

class APICount(models.Model):
    count = models.IntegerField(default= 0)

    def __str__(self) -> str:
        return f"{self.count}"
    

class chatGPTLifeLine(models.Model):
    key = models.CharField(max_length=1000)
    numUsed = models.IntegerField(default=0)
    lastUsed = models.FloatField(blank=True,null=True)
    isDepleted = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.key

    


    