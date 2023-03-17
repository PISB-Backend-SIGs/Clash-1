import json,random
from datetime import datetime,timedelta
from django.utils import timezone
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

def check_answer(u_answer,actual_answer,marks_dict,player):
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

        if (player.p_lifeline_activate):
            # score["marks_sub_to_player"]= -5
            score["score"]=-5
    return score


def set_time():
    # print(timezone.now())
    # print("inside utils",timezone.now()+timedelta(minutes=28))
    #datatime can be changed by timezone
    start_time=timezone.now()
    dict={
        "start_time":start_time,
        "end_time":start_time.astimezone(timezone.utc)+timedelta(minutes=1),
    }
    return dict

def check_lifeline_activate(player,submission,question):
    if (len(submission)>=3):
        streak = 0
        for i in range(3):
            if (submission[i].points>0):
                streak+=1
        # print("submission bool",submission[0].lifeline_activated,submission[0].lifeline_activated,submission[0].lifeline_activated)
        if (streak == 3 and not(submission[0].lifeline_activated) and not(submission[1].lifeline_activated)  and not(submission[2].lifeline_activated)):
            # print("inside if of check lifeline")
            opt_list = [1,2,3,4]
            opt_list.remove(question.q_answer)
            opt_list.pop(1)

            lifeline_dict={
                "option_disable":opt_list,
                "lifeline_activate_number":1,
                "activate":True,
                "marks_red":-5
            }
            player.p_lifeline_activate = True
            player.save()
            return lifeline_dict
        else:
            lifeline_dict={
                "activate":False
            }
            player.p_lifeline_activate = False
            player.save()
            return lifeline_dict
    else:
        lifeline_dict={
            "activate":False
        }
        player.p_lifeline_activate = False
        player.save()
        return lifeline_dict
