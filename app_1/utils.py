import json,random
from datetime import datetime,timedelta
from django.utils import timezone
from app_1.models import Lifeline
from .models import Submission
import openai
from decouple import config
size = 9     #size of question display to user
rang = 53 #size of question in database
def create_random_list(crnt_ques):
    que_list= [x for x in range(1,rang+1)]
    random.shuffle(que_list)
    print(que_list,"user total list",crnt_ques,"user crt ques")
    if crnt_ques in que_list:
        que_list.remove(crnt_ques)
    que_list = json.dumps(que_list)
    # print(type(que_list))
    # print(que_list)
    return que_list
# create_random_list()

def get_number(random_question_list):
    dictonary={}
    if (len(random_question_list) !=0 ):
        question_number = random_question_list.pop()
        print("dfsdfsdfds",question_number)
        que_list=random_question_list
        dictonary["question_number"]=question_number
        dictonary["ques_list"]=que_list
    
    else:
        dictonary["question_number"]=None
        dictonary["ques_list"]=[]

    print("DFsdfsdf",dictonary)
    return dictonary

def get_question(random_question_list,prev_que_num,pre_ans,pre_actual_ans):
    '''
    This function returns crnt question of user which is displayed to user
    and marks add and sub to that crnt question and also returns remaining question list
    '''
    marks_dict = {}
    # number = random.randint(1,10)
    question_number = get_number(random_question_list)
    print("previous","\n actual ans",pre_actual_ans,"user ans",pre_ans,"\n")
    # print(question_number)
    if (prev_que_num != 0 and pre_actual_ans!=None):
        if (pre_actual_ans == pre_ans):
            # marks_dict["streak"]=True
            marks_dict["marks_add"]= 4
            marks_dict["marks_redu"]= -2
        else:
            # marks_dict["streak"]=False
            marks_dict["marks_add"]= 2
            marks_dict["marks_redu"]= -1
    else:
        marks_dict["marks_add"]= 4
        marks_dict["marks_redu"]= -2
    marks_dict["ques_number"]=question_number["question_number"]
    marks_dict["ques_list"]=question_number["ques_list"]
    print("marks pre",marks_dict["marks_add"],marks_dict["marks_redu"],"\n")
    return marks_dict

# def isAnsCorrect(u_answer,actual_answer,marks_dict,player,user):

    
def check_answer(u_answer,actual_answer,marks_dict,player,user):
    '''
    This utils returns marks for the user's crntly solved question 
    And if lifeline is activate it gives proper marks substract
    And also return marking scheme for next question
    
    '''
    score ={}
    print("Check crt question","\nactual ans",actual_answer.questionAnswer,"\nactual ans",u_answer,"\n")
    print("marks crt",marks_dict["marks_add"],marks_dict["marks_redu"],"\n")
    if u_answer== None:
        # score["streak"]=False
        score["score"]=-1
        score["marks_add_to_player"]= 2    #to get marks for next question
        score["marks_sub_to_player"]= -1
        score["isCorrect"]=False
    elif int(u_answer) == actual_answer.questionAnswer:
        # score["streak"]=True
        score["score"]=marks_dict["marks_add"]
        score["marks_add_to_player"]=4    #to get marks for next question
        score["marks_sub_to_player"]=-2
        score["isCorrect"]=True
    else:
        # score["streak"]=False
        score["score"]=marks_dict["marks_redu"]
        score["marks_add_to_player"]= 2    #to get marks for next question
        score["marks_sub_to_player"]= -1
        score["isCorrect"]=False
        try:
            lifeline = Lifeline.objects.get(user=user,isActive=True)
            if (lifeline.lifelineID==1):
                # score["marks_sub_to_player"]= -5
                score["score"]=-5
            if (lifeline.lifelineID==2):
                # score["marks_sub_to_player"]= -5
                score["score"]=-4
        except:
            pass
    return score


def set_time():
    # print(timezone.now())
    # print("inside utils",timezone.now()+timedelta(minutes=28))
    #datatime can be changed by timezone
    start_time=timezone.now()
    dict={
        "start_time":start_time,
        "end_time":start_time.astimezone(timezone.utc)+timedelta(minutes=20),
    }
    return dict

def checkStreak(player):
    submissions = Submission.objects.filter(player=player).all()
    streak = 0
    if (len(submissions)>0):
        last3Submissions = submissions.order_by("-id")
        # print(lifeLine1Submissions.values())
        for i in range(len(submissions)):
            if (last3Submissions[i].isCorrect):
                streak+=1
            else:
                # if(i==0):
                #     streak=0
                #     break
                # else:
                #     break
                break
    return streak
    

def check_lifeline_activate(user,player,submission,question):
    '''decide the lifeline and pass its data'''
    flag=0
    opt_list=[-1]
    streak = checkStreak(player)
    if streak>=3:
        # lifeLine1Submissions = submission.order_by("-id")[:3]
        # # print(lifeLine1Submissions.values())
        # for i in range(3):
        #     if (lifeLine1Submissions[i].points>0):
        #         streak+=1
        # print("submission bool",submission[0].lifelineActivated,submission[0].lifelineActivated,submission[0].lifelineActivated)
        #condition for lifeline 1
        # if (streak == 3 and not(lifeLine1Submissions[0].lifelineActivated) and not(lifeLine1Submissions[1].lifelineActivated)  and not(lifeLine1Submissions[2].lifelineActivated)):
        if (streak >= 3 ):
            # print("inside if of check lifeline")
            opt_list = [1,2,3,4]
            opt_list.remove(question.questionAnswer)
            opt_list.pop(1)
            try:
                lifeline = Lifeline.objects.get(user=user,lifelineID =1)
            except:
                lifeline = Lifeline(user=user,lifelineID=1)
                lifeline.save()

            player.lifelineActivationFlag = True
            arr = json.loads(player.lifelineArray)
            if not(1 in arr):
                arr.append(1)
            player.lifelineArray = json.dumps(arr)
            # life_line_array = json.loads(player.lifelineArray)
            player.save()
            flag+=1
        else:
            arr = json.loads(player.lifelineArray)
            if (1 in arr):
                arr.remove(1)
            player.lifelineArray = json.dumps(arr)
            # life_line_array = json.loads(player.lifelineArray)
            player.save()

     #condition for lifeline 2  
    if(player.playerScore>7):
        try:
            lifeline = Lifeline.objects.get(user=user,lifelineID =2)
        except:
            lifeline = Lifeline(user=user,lifelineID=2)
            lifeline.save()
        if (lifeline.lifelineCounter<2):
            arr = json.loads(player.lifelineArray)
            if not(2 in arr):
                arr.append(2)
            player.lifelineArray = json.dumps(arr)
            # life_line_array = json.loads(player.lifelineArray)
            player.save()
            flag+=1

    # LifeLine3
    if( len(submission) > 2 and accuracy(submission) > 50):
        try:
            lifeline = Lifeline.objects.get(user=user,lifelineID =3)
        except:
            lifeline = Lifeline(user=user,lifelineID=3)
            lifeline.save()
        if (lifeline.lifelineCounter < 1):
            arr = json.loads(player.lifelineArray)
            if not(3 in arr):
                arr.append(3)
            player.lifelineArray = json.dumps(arr)
            # life_line_array = json.loads(player.lifelineArray)
            player.save()
            flag+=1

            
    if (flag<=0):
        lifeline_dict={
            "activate":False,
            "streak ":streak
        }
        player.lifelineActivationFlag = False
        player.save()
        return lifeline_dict
    else:
        print("sssssssssssssssss")
        
        lifeline_dict={    
            "option_disable":opt_list,
            # "lifeline_activate_number":1,
            "lifeline_activate_number":json.loads(player.lifelineArray),
            "activate":True,
            "marks_red":-5,
            'lifeline_activation_flag':lifeline.isActive,
            "streak ":streak
        }
        return lifeline_dict
    



openai.api_key = config("OPENAI_KEY")

def chatbot_response(user_input):
    '''to give output from  CHATGPT'''
    response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = user_input,
        temperature = 0.5,
        max_tokens = 1024 ,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    return response["choices"][0]["text"]

def accuracy(submissions):
    '''to get accuracy of ans submitted'''
    noofRightAns = len(submissions.filter(isCorrect = True))
    noOfQuestionsAttempted = len(submissions)
    accuracy = (noofRightAns/noOfQuestionsAttempted)*100
    print(accuracy)
    return accuracy


