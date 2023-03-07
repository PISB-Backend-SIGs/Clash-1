import app_1.views
from django.contrib.auth.models import User
from .models import Player
from datetime import date, timedelta, datetime
from django.utils import timezone

def check_time(view_func):
    def wrap(request,*args, **kwargs):
        print("inside dec username",request.user.username)
        user = User.objects.get(username=request.user)
        player = Player.objects.get(user= user)
        p_end_time = player.p_end_time.astimezone()
        end_time = datetime(year=p_end_time.year, month=p_end_time.month, day=p_end_time.day, hour=p_end_time.hour, minute=p_end_time.minute, second=p_end_time.second)
        final_time = int(end_time.timestamp())   #user end time in sec
        current_time =  int(datetime.now().timestamp())   #crrent server time in sec
        print("final time ",final_time)
        print("end time ",current_time)
        print("diff ",final_time-current_time)
        if ((final_time-current_time <0)):
            return app_1.views.submit(request)
            # return view_func(request,*args,**kwargs)
        else:
            return view_func(request,*args,**kwargs)
        # return view_func(request,*args,**kwargs)
    return wrap