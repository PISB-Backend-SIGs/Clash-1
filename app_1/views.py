from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
# from django.http import HttpResponseRedirect
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
# Create your views here.

@login_required(login_url="signin")
def home(request):
    # s= User.objects.all()
    # # s=list(s)
    # print(s.p_current_score)
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    print(player)
    print(player.p_que_list)
    
    

    context={
        "title":"Home",
        "user":request.user
    }
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        player = Player.objects.get(user=user)


        checkbox = request.POST.get("checkbox")
        if (checkbox == "checked"):
            if not(player.p_is_started):
                player.p_is_started = True
                player_time_detail = set_time()
                player.p_starting_time = player_time_detail["start_time"]
                player.p_end_time = player_time_detail["end_time"]
                player.save()
            if (player.p_is_ended):
                return redirect("result")
            return redirect("questions")
        else:
            messages.error(request, "Checkbox not checked")
            return redirect("home")
    return render(request,"app_1\home.html",context)

# from django.views.decorators.cache import never_cache

# @never_cache
@check_test_ended
@check_time

def questions(request):

    context={
        "title":"Questions",
        "flag":True
    }
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    
    # if player.p_is_ended:
    #     print("enterd in check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     return redirect("result")
    # if request.session.get('submit'):
    #     # user has already visited this page, redirect to another page
    #     return redirect('result')
    
    # shifted to down
    # try:
    #     previous_submitions = Submission.objects.filter(player=player).order_by("-id")[:3]
    #     life_line_dict = check_lifeline_activate(player,previous_submitions,Question.objects.get(q_id=player.p_current_question))
        
    # except:
    #     life_line_dict = check_lifeline_activate(player,previous_submitions,Question.objects.get(q_id=player.p_current_question))
    # player.p_lifeline_activate = life_line_dict["activate"]
    # context["life_line_dict"]=json.dumps(life_line_dict)

    # life_line_dict= check_lifeline_activate(player,Question.objects.get(q_id=player.p_current_question))
    # context["life_line_dict"]=json.dumps(life_line_dict)



    if "next" in request.POST:
        # print("next clicked")
        # try:
        #     u_option = request.POST["option"]
        # except:
        #     messages.error(request,"all questions are compelsary")
        #     return redirect("questions")
        # question_ans = Question.objects.get(q_id = player.p_current_question)        
        u_option = request.POST.get("option")
        # submission = Submission.objects.get(player=player,question_id=player.p_current_question)
        if len(Submission.objects.filter(player=player,question_id=player.p_current_question))>0:

            submission = Submission.objects.get(player=player,question_id=player.p_current_question) #shifted to up
            submission.question_answer = u_option
            
            # submission.save()
            # return redirect("questions")
        else:
            submission = Submission(player=player,question_id=player.p_current_question,question_answer=u_option)
            submission.save()

        try:
            previous_answer = Submission.objects.get(player=player,question_id=player.p_previous_question).question_answer
            actual_ans_prev_que= Question.objects.get(q_id=player.p_previous_question).q_answer  #to get actual anser of prev question
        except:
            previous_answer=None
            actual_ans_prev_que=None


        marks_dict=get_question(json.loads(player.p_que_list),player.p_previous_question,previous_answer,actual_ans_prev_que)
        user_answer_status=check_answer(u_option , Question.objects.get(q_id=player.p_current_question),marks_dict,player)
        player.p_current_score += user_answer_status["score"]
        # print(question_ans.q_answer)

        

        player.p_que_list=json.dumps(marks_dict["ques_list"])
        player.p_previous_question =  player.p_current_question 
        player.p_current_question = marks_dict["ques_number"]
        player.p_marks_add=user_answer_status["marks_add_to_player"]
        player.p_marks_sub=user_answer_status["marks_sub_to_player"]
        player.p_current_question_number +=1
        submission.points = user_answer_status["score"]
        if (player.p_lifeline_activate):
            submission.lifeline_activated = True
            player.p_lifeline_activate = False
        submission.save()
        player.save()
        return redirect("questions")

    if "nsubmit" in request.POST:
        return redirect("submit")
        # u_option = request.POST.get("option")
        # if len(Submission.objects.filter(player=player,question_id=player.p_current_question))>0:

        #     submission = Submission.objects.get(player=player,question_id=player.p_current_question)
        #     submission.question_answer = u_option
        #     submission.save()
        #     # return redirect("questions")
        # else:
        #     submission = Submission(player=player,question_id=player.p_current_question,question_answer=u_option)
        #     submission.save()

        # previous_answer = Submission.objects.get(player=player,question_id=player.p_previous_question).question_answer
        # actual_ans_prev_que= Question.objects.get(q_id=player.p_previous_question).q_answer
        
        # marks_dict=get_question(json.loads(player.p_que_list),player.p_previous_question,previous_answer,actual_ans_prev_que)
        # user_answer_status=check_answer(u_option,Question.objects.get(q_id=player.p_current_question),marks_dict)
        # player.p_current_score +=user_answer_status["score"]
        # # print(question_ans.q_answer)


        # player.p_que_list=json.dumps(marks_dict["ques_list"])
        # player.p_previous_question =  player.p_current_question 
        # player.p_current_question = marks_dict["ques_number"]

        # player.p_is_ended=True

        # player.save()

        # return redirect(result)



    # print("enter in question after nsubmit and next")
    # print(len(question),"and",player.p_current_question)
    # print(len(Submission.objects.filter(player=request.user)))

    # print(Submission.objects.filter(player=player))    #show submission query

    # try:
    if len(Submission.objects.filter(player=player))>=9:
        print("printed when submission is at 10",len(Submission.objects.filter(player=player)))
        context["flag"]=False
    # except:
    #     print("flag si true")
    #     context["flag"]=True
    # print(request.user.p_current_question)   #working

    # if player.p_current_question ==0:
    #     que_num= get_number(json.loads(player.p_que_list))
    #     print("generated jdhaskjfhkasjhf",que_num)
    #     player.p_current_question=que_num["question_number"]
    #     player.p_que_list=json.dumps(que_num["que_list"])
    #     player.save()

    #     context["question"]=Question.objects.get(q_id=que_num["question_number"])

    #chance to give error

    #to check lifeline
    # lifeline_dict = check_lifeline_activate(player,Question.objects.get(q_id=player.p_current_question))
    # if (lifeline_dict["activate"]):
    #     context["life_line_to_frontend"]=lifeline_dict

    # try:

    #     context["question"]=Question.objects.get(q_id=player.p_current_question)
    #     context["question_number"]=player.p_current_question_number
    # except:
    #     return redirect("result")
    try:
        previous_submitions = Submission.objects.filter(player=player).order_by("-id")[:3]
        life_line_dict = check_lifeline_activate(player,previous_submitions,Question.objects.get(q_id=player.p_current_question))
    except:
        life_line_dict = {"activate":False}
    # player.p_lifeline_activate = life_line_dict["activate"]
    context["life_line_dict"]=json.dumps(life_line_dict)

    context["question"]=Question.objects.get(q_id=player.p_current_question)
    context["question_number"]=player.p_current_question_number
    
    context["player"]=player
    context["marking_scheme"]={"marks_add":player.p_marks_add,"marks_sub":player.p_marks_sub}
    print("time going to f",player.p_end_time.astimezone())
    context['player_time']=str(player.p_end_time.astimezone())
    return render(request,"app_1\questions.html",context)

# @check_time
@check_test_ended
def submit(request):
    request.session['submit'] = True
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    # if player.p_is_ended:
    #     return redirect("result")
    if player.p_is_started:
        if player.p_is_ended:
            return redirect("result")
        u_option = request.POST.get("option")
        if len(Submission.objects.filter(player=player,question_id=player.p_current_question))>0:
            submission = Submission.objects.get(player=player,question_id=player.p_current_question)
            submission.question_answer = u_option
            submission.save()
            # return redirect("questions")
        else:
            submission = Submission(player=player,question_id=player.p_current_question,question_answer=u_option)
            submission.save()
        previous_answer = Submission.objects.get(player=player,question_id=player.p_previous_question).question_answer
        actual_ans_prev_que= Question.objects.get(q_id=player.p_previous_question).q_answer
        
        marks_dict=get_question(json.loads(player.p_que_list),player.p_previous_question,previous_answer,actual_ans_prev_que)
        user_answer_status=check_answer(u_option,Question.objects.get(q_id=player.p_current_question),marks_dict,player)
        player.p_current_score +=user_answer_status["score"]
        # print(question_ans.q_answer)
        player.p_que_list=json.dumps(marks_dict["ques_list"])
        player.p_previous_question =  player.p_current_question 
        player.p_current_question = marks_dict["ques_number"]
        player.p_is_ended=True
        submission.points = user_answer_status["score"]

        if (player.p_lifeline_activate):
            submission.lifeline_activated = True
            player.p_lifeline_activate = False

        player.save()
        submission.save()

        # return redirect(result)
        return HttpResponseRedirect("/result/")


@login_required(login_url="signin")
def result(request):
    context={
        "title":"Result",
    }
    player = Player.objects.get(user=request.user)
    context["player"]=player
    return render(request,"app_1\\result.html",context)



def signin(request):
    # print(player.p_que_list)
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
            # print(player,player.p_is_ended)
            if not(player.p_is_ended) :
                login(request, user)
                # player = User.objects.get(username=request.user)
                # print(player.p_que_list)
               
                if not(player.p_que_list) or (player.p_que_list=="")  :
                    # print("if inntrye")
                    player.p_que_list = create_random_list(player.p_current_question)
                    player.save()

                if request.user.is_superuser:
                    return redirect("settingwale")
            # fname = user.first_name
                return redirect("home")
            else:
                messages.error(request,"You already give test")

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
            return redirect('home')

        # if User.objects.filter(email=email):
        #     messages.error(request,"Email Already Registered!")
        #     return redirect('home')

        if len(username)<3:
            messages.error(request,"Username must be atleast 3 characters")

        if pass1 != pass2:
            messages.error(request,"Passwords did not match")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric")
            return redirect('home')

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

          
    #gives too many errors to redirect it on same page    
    # else:
    #     messages.error(request,"User Registration Failed")
    #     return redirect('signup')

    return render(request,"app_1/signup.html")




@login_required(login_url='login')
def settingwale(request):
    context={}
    players = Player.objects.all()
    # users = User.objects.all()
    context["players"]=players
    # context["users"]=users
    return render(request,"app_1/settingwale.html",context)



#To handle 404 error if user try to access diff page
def error_404(request, exception):
    return render(request, 'errors\error_404.html',{"exception":"404"})
# def error_500(request, exception):
#     return render(request, 'errors\error_404.html',{"exception":"500"})


def test(request):
    user= User.objects.get(username = "testuser94")
    player = Player.objects.get(user=user)
    submission=Submission.objects.filter(player=player).order_by("-id")[:3].values_list()
    print(submission)
    return render(request,"app_1/test.html")