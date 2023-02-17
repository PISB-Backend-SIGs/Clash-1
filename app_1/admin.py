from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class ExtraFieldAdmin(UserAdmin):
    model = ExtraField
    add_form = ExtraFieldForm
    fieldsets=(
        *UserAdmin.fieldsets,(
            "Player",{
                "fields":(
                    "p_current_score",
                    "p_current_question",
                    "p_previous_question",
                    "p_starting_time"
                )
            }
        )
    )
admin.site.register(ExtraField,ExtraFieldAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display=[
        "q_id"
    ]
admin.site.register(Question,QuestionAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    list_display=[
        "player","question_id","question_answer","points"
    ]
admin.site.register(Submission,SubmissionAdmin)