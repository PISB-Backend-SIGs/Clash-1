from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import random 

# Create your models here.
class Player(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    p_current_score = models.IntegerField(blank=True,default=0)
    p_que_list=models.TextField(null=True,blank=True)
    p_current_question = models.IntegerField(default=random.randint(1,11),null=True,blank=True)  #random question number of player
    p_current_question_number = models.IntegerField(default=1)                                   #number visible to user sequentialy
    p_is_started=models.BooleanField(default=False)              #to check user started quizz or not 
    p_is_ended=models.BooleanField(default=False)              #to check user started quizz or not 
    p_previous_question = models.IntegerField(blank=True,default=0)
    p_starting_time = models.DateTimeField(null=True,blank=True)  #actual starting time
    p_end_time = models.DateTimeField(null=True,blank=True)  #game current time
    p_marks_add=models.IntegerField(null=True,blank=True,default=4)  #marks add
    p_marks_sub=models.IntegerField(null=True,blank=True,default=-2) #marks sub

    def __str__(self) -> str:
        return f"{self.user}"
    
    
class Question(models.Model):
    q_id = models.IntegerField(unique=True,primary_key=True)
    question = models.TextField()

    q_option_1 = models.TextField()
    q_option_2 = models.TextField()
    q_option_3 = models.TextField()
    q_option_4 = models.TextField()

    q_answer = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.q_id}"

class Submission(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    question_id = models.IntegerField()
    question_answer = models.IntegerField(null=True)
    points = models.IntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.player}"