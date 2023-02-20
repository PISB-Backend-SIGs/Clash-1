from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
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

    # print(len(question),"and",player.p_current_question)
    if player.p_current_question >=len(question):
        context["flag"]=False
    # print(request.user.p_current_question)   #working
    context["question"]=Question.objects.get(q_id=player.p_current_question)
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
            fname = user.first_name
            return render(request, "app_1/home.html",{'fname':fname} )

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

        if len(username)>15:
            messages.error(request,"Username must be under 15 characters")

        if pass1 != pass2:
            messages.error(request,"Passwords did not match")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric")
            return redirect('home')

        myuser = ExtraField.objects.create_user(username, email, pass1) #register user in backend
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save() #save user in database

        messages.success(request, "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")
        return redirect('signin')


    return render(request,"app_1/signup.html")




@login_required(login_url='login')
def settingwale(request):
    context={}
    players = ExtraField.objects.all()
    # users = User.objects.all()
    context["players"]=players
    # context["users"]=users
    return render(request,"app_1/settingwale.html",context)