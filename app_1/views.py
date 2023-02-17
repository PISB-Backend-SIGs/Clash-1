from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    # s= ExtraField.objects.all()
    # # s=list(s)
    # print(s.p_current_score)
    # player = ExtraField.objects.get(username="prasad")
    # print(player)
    # print(player.p_current_question)
    return HttpResponse("Hello world")


def questions(request):
    context={
        "title":"Questions",
        "flag":True
    }
    player = ExtraField.objects.get(username=request.user)
    question = Question.objects.all() 
    # print(player)
    
    if "next" in request.POST:
        print("next clicked")
        player.p_current_question += 1
        player.p_previous_question += 1 
        player.save()
    if "nsubmit" in request.POST:
        # player.p_current_question += 1
        # player.p_previous_question += 1 
        # player.save()
        return redirect(result)

    print(len(question),"and",player.p_current_question)
    if player.p_current_question >=len(question):
        context["flag"]=False
    # print(request.user.p_current_question)   #working
    context["question"]=Question.objects.get(q_id=player.p_current_question)
    return render(request,"app_1\questions.html",context)

def result(request):
    context={
        "title":"Result",
    }
    player = ExtraField.objects.get(username=request.user)
    context["player"]=player
    return render(request,"app_1\esult.html",context)
