import json,random
from datetime import datetime,timedelta
from django.utils import timezone
size = 10      #size of question display to user
rang = size+1 #size of question in database

# def check_lifeline_activate(player,submission,question):
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

    # logic for 2nd lifeline

# for post method
# def create_blog_post(request):
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return HttpResponse('option changed successfully')
#     else:
#         form = BlogPostForm()
#     return render(request, 'create_blog_post.html', {'form': form})

# for get method
# def create_blog_post(request):
#     if request.method == 'GET':
#         form = BlogPostForm()
#         return render(request, 'create_blog_post.html', {'form': form})
#     elif request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return HttpResponse('Option changed successfully successfully')
#     return HttpResponse('Invalid request')


