from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
import re
from .utils import *
from django.http import JsonResponse
from datetime import datetime,timedelta
from .decorators import *
from .utils import *
# Create your views here.
def signin(request):
    # check(Question.objects.all())
    if request.method == "POST":   #For signin page only username and pass1 taken
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password= pass1)         #authenticate user here

        if user is not None :  #IF correct credentials given
            # player = Player.objects.get(user=user)
            try:
                player = Player.objects.get(user=user)
            except:
                player = Player(user=user)
                player.save()
                player = Player.objects.get(user=user)
            # (player,player.p_is_ended)
            if not(player.p_is_ended) :
                login(request, user)
                # player = User.objects.get(username=request.user)
               
                if not(player.p_que_list) or (player.p_que_list=="")  :
                    player.p_que_list = create_random_list(player.p_current_question)
                    player.save()
                return redirect("home")
            else:
                messages.error(request,"You already given the test")

        else:  #If wrong credentials given
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request,"app_1/login.html")

def index(request):
    context={
        "title":"Home page"
    }
    return render(request,"app_1\mainhome.html",context)

# @login_required(login_url="signin")
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect("index")
    else:
        return redirect('signin')

def signup(request):
    
    if request.method == "POST": #Create user details to take them input
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']  #For storing pass2

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists ! PLease try Different username")
            return redirect('signup')

        if len(username)<3:
            messages.error(request,"Username must be atleast 3 characters")

        if pass1 != pass2:
            messages.error(request,"Passwords did not match")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric")
            return redirect('signup')

        if len(pass1)>8:
                if re.search('[A-Z]', pass1)!=None and re.search('[0-9]', pass1)!=None and re.search("^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", pass1)!=None:
                    
                    myuser = User.objects.create_user(username, email, pass1) #register user in backend
                    myuser.first_name = fname
                    myuser.last_name = lname
                    player = Player(user=myuser)
                    player.save()
                    myuser.save() #save user in database
                    
                    messages.success(request, "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")
                    return redirect('signin')
        else:
                messages.error(request, "Password must contain atleast one number, one  special character and one capital letter")
                return redirect('signup')

    return render(request,"app_1/signup.html")

def index(request): #diplayed before login and after logout
    context={ "title":"Home page" }
    return render(request,"app_1\mainhome.html",context)

@login_required(login_url="signin")
def home(request):
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    context={
        "title":"Home",
        "user":request.user
    }
    if request.method == "POST":
        checkbox = request.POST.get("checkbox")
        if (checkbox == "checked"):
            if not(player.isStarted):
                player.isStarted = True
                playerTimeDetails = set_time()
                player.startTime = playerTimeDetails["start_time"]
                player.endTime = playerTimeDetails["end_time"]
                player.save()
            if (player.isEnded):
                return redirect("result")
            return redirect("questions")
        else:
            messages.error(request, "Checkbox not checked")
            return redirect("home")
    return render(request,"core\home.html",context)



#for not allowing to access questins after submitting the test
from django.views.decorators.cache import never_cache
@never_cache
@check_test_ended
@check_time

def questions(request):

    context={
        "title":"Questions",
        "flag":True  #for last question converting next to submit
    }
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    
    #it handles user next question
    if "next" in request.POST:       
        userSelectedOption = request.POST.get("option")
        #This is for if user get question which already done 
        if len(Submission.objects.filter(player=player,questionNumber = player.questionNumber ) )>0:

            submission = Submission.objects.get(player=player,questionNumber=player.questionNumber)
        else:
            submission = Submission(player=player,questionNumber=player.questionNumber,questionAnswer = userSelectedOption, questionIndex = player.questionIndex)
            submission.save()

        #To check marking scheme
        try:
            previousAnswerByUser = Submission.objects.get(player=player,question_id=player.p_previous_question).question_answer
            previousActualAnswer = Question.objects.get(q_id=player.p_previous_question).q_answer  #to get actual anser of prev question
        except:
            previousAnswerByUser=None
            previousActualAnswer =None


        marks_dict=get_question(json.loads(player.p_que_list),player.p_previous_question,previousAnswerByUser,previousActualAnswer )   #it returns marks next question and question number
        user_answer_status=check_answer(u_option , Question.objects.get(q_id=player.p_current_question),marks_dict,player,user)  #it checks ans of crnt question
        player.p_current_score += user_answer_status["score"]
        player.p_que_list=json.dumps(marks_dict["ques_list"])
        player.p_previous_question =  player.p_current_question 
        player.p_current_question = marks_dict["ques_number"]
        player.p_marks_add=user_answer_status["marks_add_to_player"]
        player.p_marks_sub=user_answer_status["marks_sub_to_player"]
        player.p_current_question_number +=1
        submission.points = user_answer_status["score"]
        try:
            lifeline = Lifeline.objects.get(user=user,is_active=True)
            if (lifeline.is_active):
                submission.lifeline_activated = True
                lifeline.is_active = False
                lifeline.save()
                player.p_lifeline_activate = False
                array=json.loads(player.p_lifeline_array )
                # array.remove(lifeline.lifeline_id)
                # if(1 in array):
                #     array.remove(1)
                array.clear()
                player.p_lifeline_array = json.dumps(array)
                player.save()
        except:
            array=json.loads(player.p_lifeline_array )
            if (1 in array):
                submission.lifeline_activated = True
                array.remove(1)
            player.p_lifeline_array = json.dumps(array)
            player.save()
            
        submission.save()
        player.save()
        return redirect("questions")

    #it handle users submit 
    if "nsubmit" in request.POST:
        u_option = request.POST.get("option")
        if len(Submission.objects.filter(player=player,question_id=player.p_current_question))>0:
            submission = Submission.objects.get(player=player,question_id=player.p_current_question)
            submission.question_answer = u_option
            submission.save()
            # return redirect("questions")
        else:
            submission = Submission(player=player,question_id=player.p_current_question,question_answer=u_option,sequential_ques_id=player.p_current_question_number)
            submission.save()
        return redirect("submit")
        
    if len(Submission.objects.filter(player=player))>=9:
        context["flag"]=False
    try:
        previous_submitions = Submission.objects.filter(player=player).all()
        life_line_dict = check_lifeline_activate(user,player,previous_submitions,Question.objects.get(q_id=player.p_current_question))
    except:
        life_line_dict = {"activate":False}
    try:
        context["which_lifeline_is_active"]=Lifeline.objects.get(user=user,is_active=True)
    except:
        pass
    context["life_line_dict"]=json.dumps(life_line_dict)
    
    context["wrong_question_list"]=[x.sequential_ques_id for x in Submission.objects.filter(player=player) if x.points<0]

    context["question"]=Question.objects.get(q_id=player.p_current_question)
    context["question_number"]=player.p_current_question_number
    
    context["player"]=player
    context["marking_scheme"]={"marks_add":player.p_marks_add,"marks_sub":player.p_marks_sub}
    context['player_time']=str(player.p_end_time.astimezone())
    return render(request,"app_1\questions.html",context)