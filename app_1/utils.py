import json,random
from datetime import datetime,timedelta
from django.utils import timezone
from app_1.models import Lifeline
size = 10      #size of question display to user
rang = size+1 #size of question in database
def create_random_list(crnt_ques):
    que_list= random.sample(range(1,rang),size)
    print(que_list,"user total list",crnt_ques,"user crt ques")
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

def check_answer(u_answer,actual_answer,marks_dict,player,user):
    score ={}
    print("Check crt question","\nactual ans",actual_answer.q_answer,"\nactual ans",u_answer,"\n")
    print("marks crt",marks_dict["marks_add"],marks_dict["marks_redu"],"\n")
    if u_answer== None:
        # score["streak"]=False
        score["score"]=-1
        score["marks_add_to_player"]= 2    #to get marks for next question
        score["marks_sub_to_player"]= -1
    elif int(u_answer) == actual_answer.q_answer:
        # score["streak"]=True
        score["score"]=marks_dict["marks_add"]
        score["marks_add_to_player"]=4    #to get marks for next question
        score["marks_sub_to_player"]=-2
    else:
        # score["streak"]=False
        score["score"]=marks_dict["marks_redu"]
        score["marks_add_to_player"]= 2    #to get marks for next question
        score["marks_sub_to_player"]= -1
        try:
            lifeline = Lifeline.objects.get(user=user,is_active=True)
            if (lifeline.lifeline_id==1):
                # score["marks_sub_to_player"]= -5
                score["score"]=-5
            if (lifeline.lifeline_id==2):
                # score["marks_sub_to_player"]= -5
                score["score"]=-6
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
        "end_time":start_time.astimezone(timezone.utc)+timedelta(minutes=10),
    }
    return dict




def check_lifeline_activate(user,player,submission,question):
    flag=0
    opt_list=[-1]
    streak = 0
    if (len(submission)>=3):
        
        for i in range(3):
            if (submission[i].points>0):
                streak+=1
        # print("submission bool",submission[0].lifeline_activated,submission[0].lifeline_activated,submission[0].lifeline_activated)
        if (streak == 3 and not(submission[0].lifeline_activated) and not(submission[1].lifeline_activated)  and not(submission[2].lifeline_activated)):
            # print("inside if of check lifeline")
            opt_list = [1,2,3,4]
            opt_list.remove(question.q_answer)
            opt_list.pop(1)
            try:
                lifeline = Lifeline.objects.get(user=user,lifeline_id =1)
            except:
                lifeline = Lifeline(user=user,lifeline_id=1)
                lifeline.save()

            player.p_lifeline_activate = True
            arr = json.loads(player.p_lifeline_array)
            if not(1 in arr):
                arr.append(1)
            player.p_lifeline_array = json.dumps(arr)
            # life_line_array = json.loads(player.p_lifeline_array)
            player.save()
            
            # lifeline_dict["option_disable"]=opt_list,
            # # "lifeline_activate_number":1,
            # lifeline_dict["lifeline_activate_number"]=json.loads(player.p_lifeline_array),
            # lifeline_dict["activate"]=True,
            # lifeline_dict["marks_red"]=-5,
            # lifeline_dict['lifeline_activation_flag']=lifeline.is_active

            flag+=1
        
    if(player.p_current_score>7):
        try:
            lifeline = Lifeline.objects.get(user=user,lifeline_id =2)
        except:
            lifeline = Lifeline(user=user,lifeline_id=2)
            lifeline.save()
        if (lifeline.number_of_lifeline<2):
            arr = json.loads(player.p_lifeline_array)
            if not(2 in arr):
                arr.append(2)
            player.p_lifeline_array = json.dumps(arr)
            # life_line_array = json.loads(player.p_lifeline_array)
            player.save()
            # lifeline_dict["lifeline_activate_number"]=json.loads(player.p_lifeline_array),
            # lifeline_dict["activate"]=True,
            # lifeline_dict["marks_red"]=-5,
            # lifeline_dict['lifeline_activation_flag']=lifeline.is_active
            flag+=1
    print("sdsssssssssssssssssssssss",flag)
    if (flag<=0):
        
        lifeline_dict={
            "activate":False,
            "streak ":streak
        }
        
        player.p_lifeline_activate = False
        player.save()
        return lifeline_dict
    else:
        print("sssssssssssssssss")
        
        lifeline_dict={    
            "option_disable":opt_list,
            # "lifeline_activate_number":1,
            "lifeline_activate_number":json.loads(player.p_lifeline_array),
            "activate":True,
            "marks_red":-5,
            'lifeline_activation_flag':lifeline.is_active,
            "streak ":streak
        }
        return lifeline_dict

