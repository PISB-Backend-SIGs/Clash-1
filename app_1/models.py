from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.
class ExtraField(AbstractUser):
    p_current_score = models.IntegerField(blank=True,default=0)
    p_current_question = models.IntegerField(blank=True,default=0)
    p_starting_time = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.username
    
    
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
    player = models.ForeignKey(ExtraField, on_delete=models.CASCADE)
    question_id = models.IntegerField()
    question_answer = models.IntegerField(null=True)
    points = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.player}"