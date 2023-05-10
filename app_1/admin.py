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
#                     "playerScore",
#                     "questionList",
#                     "questionIndex",
#                     "questionNumber",
#                     "previousQuestion",
#                     "startTime",
#                     "isStarted",
#                     "marksAdd",
#                     "marksSubstract",
#                 )
#             }
#         )
#     )
class PlayerAdmin(admin.ModelAdmin):
    list_display=[
        "user",
        "isTeam",
        "playerScore",
        "questionList",
        "questionIndex",
        "questionNumber",
        "previousQuestion",
        "startTime",
        "EndTime",
        "isStarted",
        "isEnded",
        "lifelineActivationFlag",
        "marksAdd",
        "marksSubstract",
    ]
admin.site.register(Player,PlayerAdmin)



class LifelineAdmin(admin.ModelAdmin):
    list_display=[
        "user","lifelineID","isActive"
    ]
admin.site.register(Lifeline,LifelineAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display=[
        "questionID","questionNumber","questionAnswer"
    ]
admin.site.register(Question,QuestionAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    list_display=[
        "player","questionID","userOption","points","lifelineActivated","isCorrect"
    ]
admin.site.register(Submission,SubmissionAdmin)


class APICountAdmin(admin.ModelAdmin):
    list_display=[
        "count"
    ]
admin.site.register(APICount,APICountAdmin)