from django.contrib import admin
from .models import *
from .forms import *
# from django.contrib.auth.admin import UserAdmin
# Register your models here.

# class UserAdmin(UserAdmin):
#     model = User
#     add_form = User
#     fieldsets=(
#         *UserAdmin.fieldsets,(
#             "Player",{
#                 "fields":(
#                     "p_current_score",
#                     "p_que_list",
#                     "p_current_question_number",
#                     "p_current_question",
#                     "p_previous_question",
#                     "p_starting_time",
#                     "p_is_started",
#                     "p_marks_add",
#                     "p_marks_sub",
#                 )
#             }
#         )
#     )
class PlayerAdmin(admin.ModelAdmin):
    list_display=[
        "user","p_current_score",
        "p_que_list",
        "p_current_question_number",
        "p_current_question",
        "p_previous_question",
        "p_starting_time",
        "p_is_started",
        "p_marks_add",
        "p_marks_sub",
    ]
admin.site.register(Player,PlayerAdmin)



class QuestionAdmin(admin.ModelAdmin):
    list_display=[
        "q_id","q_answer"
    ]
admin.site.register(Question,QuestionAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    list_display=[
        "player","question_id","question_answer","points"
    ]
admin.site.register(Submission,SubmissionAdmin)