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
# Create your views here.

#Users home page after login
@login_required(login_url="signin")
def home(request):
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    # print(player)
    # print(player.p_que_list)
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
#for not allowing to access questins after submitting the test
from django.views.decorators.cache import never_cache
@never_cache
@check_test_ended
@check_time

def questions(request):

    context={
        "title":"Questions",
        "flag":True
    }
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    
    #it handles user next question
    if "next" in request.POST:       
        u_option = request.POST.get("option")
        print("user option on next",u_option)
        #This is for if user get question which already done 
        if len(Submission.objects.filter(player=player,question_id=player.p_current_question))>0:

            submission = Submission.objects.get(player=player,question_id=player.p_current_question) #shifted to up
            submission.question_answer = u_option
        else:
            submission = Submission(player=player,question_id=player.p_current_question,question_answer=u_option,sequential_ques_id=player.p_current_question_number)
            submission.save()

        #To check marking scheme
        try:
            previous_answer = Submission.objects.get(player=player,question_id=player.p_previous_question).question_answer
            actual_ans_prev_que= Question.objects.get(q_id=player.p_previous_question).q_answer  #to get actual anser of prev question
        except:
            previous_answer=None
            actual_ans_prev_que=None


        marks_dict=get_question(json.loads(player.p_que_list),player.p_previous_question,previous_answer,actual_ans_prev_que)   #it returns marks next question and question number
        user_answer_status=check_answer(u_option , Question.objects.get(q_id=player.p_current_question),marks_dict,player,user)  #it checks ans of crnt question
        player.p_current_score += user_answer_status["score"]
        # print(question_ans.q_answer)

        

        player.p_que_list=json.dumps(marks_dict["ques_list"])
        player.p_previous_question =  player.p_current_question 
        player.p_current_question = marks_dict["ques_number"]
        player.p_marks_add=user_answer_status["marks_add_to_player"]
        player.p_marks_sub=user_answer_status["marks_sub_to_player"]
        player.p_current_question_number +=1
        submission.points = user_answer_status["score"]
        try:
            lifeline = Lifeline.objects.get(user=user,is_active=True)
            print(lifeline,"checking is activatd")
            if (lifeline.is_active):
                submission.lifeline_activated = True
                lifeline.is_active = False
                lifeline.save()
                player.p_lifeline_activate = False
                array=json.loads(player.p_lifeline_array )
                print("player lifeline array",array)
                # array.remove(lifeline.lifeline_id)
                # if(1 in array):
                #     array.remove(1)
                array.clear()
                print("player lifeline array after deletion",array)
                player.p_lifeline_array = json.dumps(array)
                player.save()
        except:
            array=json.loads(player.p_lifeline_array )
            print(array,"kljdlkdjlkjlk")
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
        print("user option on time  ",u_option)
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
        print("printed when submission is at 10",len(Submission.objects.filter(player=player)))
        context["flag"]=False

    #to check lifeline
    # lifeline_dict = check_lifeline_activate(player,Question.objects.get(q_id=player.p_current_question))
    # if (lifeline_dict["activate"]):
    #     context["life_line_to_frontend"]=lifeline_dict
    try:
        # previous_submitions = Submission.objects.filter(player=player).order_by("-id")[:3]
        previous_submitions = Submission.objects.filter(player=player).all()
        life_line_dict = check_lifeline_activate(user,player,previous_submitions,Question.objects.get(q_id=player.p_current_question))
    except:
        life_line_dict = {"activate":False}
    # player.p_lifeline_activate = life_line_dict["activate"]
    try:
        context["which_lifeline_is_active"]=Lifeline.objects.get(user=user,is_active=True)
    except:
        pass
    print("ssssssssssssssssssssssssssssssssssss",life_line_dict)
    context["life_line_dict"]=json.dumps(life_line_dict)
    
    context["wrong_question_list"]=[x.sequential_ques_id for x in Submission.objects.filter(player=player) if x.points<0]
    print("jjjjjjjjjjjjjjjjjjjjjj",context["wrong_question_list"])

    context["question"]=Question.objects.get(q_id=player.p_current_question)
    context["question_number"]=player.p_current_question_number
    
    context["player"]=player
    context["marking_scheme"]={"marks_add":player.p_marks_add,"marks_sub":player.p_marks_sub}
    print("time going to f",player.p_end_time.astimezone())
    context['player_time']=str(player.p_end_time.astimezone())
    return render(request,"app_1\questions.html",context)



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def lifelineActivation(request):
    # print(user,"in checklifeline async")
    if request.method == "POST":
        lifeline_id_from_frontend = request.POST.get("number")
        userr =request.POST.get("user")
        user = User.objects.get(username=userr)
        print(lifeline_id_from_frontend,"in url async")
        if(int(lifeline_id_from_frontend)==1):
            lifeline = Lifeline.objects.get(user=user,lifeline_id=lifeline_id_from_frontend)
            lifeline.is_active = True
            lifeline.number_of_lifeline +=1
            lifeline.save()
            return JsonResponse({"status":1})
        elif(int(lifeline_id_from_frontend)==2):
            player=Player.objects.get(user=user)
            arr = json.loads(player.p_que_list)
            if not(player.p_current_question in arr):
                arr.append(player.p_current_question)
                player.p_que_list = json.dumps(arr)
            ques_num =int(request.POST.get("ques_num"))
            print(type(ques_num),"Sssssssssssssssssskjh")
            player.p_current_question_number -=1
            submission = Submission.objects.get(player=player,sequential_ques_id=ques_num)
            question = Question.objects.get(q_id=submission.question_id)
            player.p_current_question=submission.question_id
            player.save()
            question_details={
                "question_title":question.question,
                "opt1":question.q_option_1,
                "opt2":question.q_option_2,
                "opt3":question.q_option_3,
                "opt4":question.q_option_4,
            }
            lifeline = Lifeline.objects.get(user=user,lifeline_id=lifeline_id_from_frontend)
            lifeline.is_active = True
            lifeline.number_of_lifeline +=1
            lifeline.save()
            return JsonResponse({"status":1,"question":question_details,"user_answer":submission.question_answer})

    else:
        return JsonResponse({"status":0})

    

# @check_time
@check_test_ended
def submit(request):
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    # if player.p_is_ended:
    #     return redirect("result")
    if player.p_is_started:
        if player.p_is_ended:
            return redirect("result")
        # u_option = request.POST.get("option")
        try:
            submission = Submission.objects.get(player=player,question_id=player.p_current_question)
            u_option = submission.question_answer
        except:
            u_option=None

        
        try:
            previous_answer = Submission.objects.get(player=player,question_id=player.p_previous_question).question_answer
            actual_ans_prev_que= Question.objects.get(q_id=player.p_previous_question).q_answer  #to get actual anser of prev question
        except:
            previous_answer=None
            actual_ans_prev_que=None
        # previous_answer = Submission.objects.get(player=player,question_id=player.p_previous_question).question_answer
        # actual_ans_prev_que= Question.objects.get(q_id=player.p_previous_question).q_answer
        
        marks_dict=get_question(json.loads(player.p_que_list),player.p_previous_question,previous_answer,actual_ans_prev_que)
        user_answer_status=check_answer(u_option,Question.objects.get(q_id=player.p_current_question),marks_dict,player,user)
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
            return redirect('home')

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
    user= User.objects.get(username = "testfuck")
    player = Player.objects.get(user=user)
    life_line_array = json.loads(player.p_lifeline_array)
    
    # player.p_lifeline_array = json.dumps([1,2])
    # life_line_array = json.loads(player.p_lifeline_array)
    print(life_line_array)
    print(type(life_line_array))
    print(type(life_line_array))
    # submission=Submission.objects.filter(player=player).order_by("-id")[:3].values_list()
    # print(submission)
    return render(request,"app_1/test.html")
    
@csrf_exempt
def test1(request):
    print("in test1")

    if request.method == "POST":
        lid = request.POST.get("number")
        print(lid)
        return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":0})