import json,random
from datetime import datetime,timedelta
from django.utils import timezone
size = 10      #size of question display to user
range = size+1 #size of question in database
def create_random_list(crnt_ques):
    que_list= random.sample(range(1,range),size)
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
            marks_dict["marks_add"]= 4
            marks_dict["marks_redu"]= -2
        else:
            marks_dict["marks_add"]= 2
            marks_dict["marks_redu"]= -1
    else:
        marks_dict["marks_add"]= 4
        marks_dict["marks_redu"]= -2
    marks_dict["ques_number"]=question_number["question_number"]
    marks_dict["ques_list"]=question_number["ques_list"]
    print("marks pre",marks_dict["marks_add"],marks_dict["marks_redu"],"\n")
    return marks_dict

def check_answer(u_answer,actual_answer,marks_dict):
    score ={}
    print("Check crt question","\nactual ans",actual_answer.q_answer,"\nactual ans",u_answer,"\n")
    print("marks crt",marks_dict["marks_add"],marks_dict["marks_redu"],"\n")
    if u_answer== None:
        score["score"]=-1
        score["marks_add_to_player"]= 2    #to get marks for next question
        score["marks_sub_to_player"]= -1
    elif int(u_answer) == actual_answer.q_answer:
        score["score"]=marks_dict["marks_add"]
        score["marks_add_to_player"]=4    #to get marks for next question
        score["marks_sub_to_player"]=-2
    else:
        score["score"]=marks_dict["marks_redu"]
        score["marks_add_to_player"]= 2    #to get marks for next question
        score["marks_sub_to_player"]= -1
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
