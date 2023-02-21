from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
import re
# Create your views here.
@login_required(login_url="signin")
def home(request):
    # s= ExtraField.objects.all()
    # # s=list(s)
    # print(s.p_current_score)
    # player = ExtraField.objects.get(username="prasad")
    # print(player)
    # print(player.p_current_question)
    context={
        "title":"Home",
        "user":request.user
    }
    if request.method == "POST":
        checkbox = request.POST.get("checkbox")
        if checkbox == "checked":
            return redirect("questions")
        else:
            messages.error(request, "Checkbox not checked")
            return redirect("home")
    return render(request,"app_1\home.html",context)

@login_required(login_url="signin")
def questions(request):
    context={
        "title":"Questions",
        "flag":True
    }
    player = ExtraField.objects.get(username=request.user)
    question = Question.objects.all() 
    # print(player)
    # user_ans = request.POST.get("option")
    # print(user_ans)
    # print(player.p_previous_question)
    # print(player.p_current_question)
    # question_ans = Question.objects.get(q_id = player.p_previous_question)
    # print(question_ans.q_answer)
    # if question_ans.q_answer == user_ans:
    #     player.p_current_score +=1
    # elif None == user_ans:
    #     player.p_current_score +=0
    # else:
    #     player.p_current_score -=1
    # player.save()

    # print("enter in question")
    if "next" in request.POST:
        # print("next clicked")
        try:
            u_option = request.POST["option"]
        except:
            messages.error(request,"all questions are compelsary")
            return redirect("questions")

        question_ans = Question.objects.get(q_id = player.p_current_question)
        # print(question_ans.q_answer)
        if u_option and int(question_ans.q_answer) == int(u_option):
            player.p_current_score +=1
        else:
            player.p_current_score -=1
        print(u_option,question_ans.q_answer)

        submission = Submission(player=request.user,question_id=player.p_current_question,question_answer=u_option)
        submission.save()

        player.p_current_question += 1
        player.p_previous_question += 1 
        player.save()
        return redirect("questions")
    if "nsubmit" in request.POST:
        # player.p_current_question += 1
        # player.p_previous_question += 1 
        # player.save()
        u_option = request.POST["option"]

        question_ans = Question.objects.get(q_id = player.p_current_question)
        # print(question_ans.q_answer)
        if u_option and int(question_ans.q_answer) == int(u_option):
            player.p_current_score +=1
        else:
            player.p_current_score -=1
        print(u_option,question_ans.q_answer)
        player.save()

        submission = Submission(player=request.user,question_id=player.p_current_question,question_answer=u_option)
        submission.save()
        return redirect(result)
    # print("enter in question after nsubmit and next")
    # print(len(question),"and",player.p_current_question)
    if player.p_current_question >=len(question):
        context["flag"]=False
    # print(request.user.p_current_question)   #working
    context["question"]=Question.objects.get(q_id=player.p_current_question)
    context["player"]=player
    return render(request,"app_1\questions.html",context)


@login_required(login_url="signin")
def result(request):
    context={
        "title":"Result",
    }
    player = ExtraField.objects.get(username=request.user)
    context["player"]=player
    return render(request,"app_1\\result.html",context)



def signin(request):

    if request.method == "POST":   #For signin page only username and pass1 taken
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password= pass1)         #authenticate user here

        if user is not None:  #IF correct credentials given
            login(request, user)
            if request.user.is_superuser:
                return redirect("settingwale")
            # fname = user.first_name
            return redirect("home")

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

        if ExtraField.objects.filter(username=username):
            messages.error(request,"Username already exists ! PLease try Different username")
            return redirect('home')

        # if ExtraField.objects.filter(email=email):
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
                    
                    myuser = ExtraField.objects.create_user(username, email, pass1) #register user in backend
                    myuser.first_name = fname
                    myuser.last_name = lname
                    myuser.save() #save user in database
                    
                    messages.success(request, "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")
                    return redirect('signin')
        else:
                messages.error(request, "Password must contain atleast one number, one  special character and one capital letter")
                return redirect('signup')
                    
    # else:
    #     messages.error(request,"User Registration Failed")
    #     return redirect('signup')

    return render(request,"app_1/signup.html")




@login_required(login_url='login')
def settingwale(request):
    context={}
    players = ExtraField.objects.all()
    # users = User.objects.all()
    context["players"]=players
    # context["users"]=users
    return render(request,"app_1/settingwale.html",context)