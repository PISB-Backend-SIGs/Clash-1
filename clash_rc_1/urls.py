"""clash_rc_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import app_1.views 
urlpatterns = [
    path('wadhivv/', admin.site.urls),
    path('', include('app_1.urls')),
]

# from django.conf.urls import handler400, handler403, handler404, handler500
# 404 not found error
handler404 = 'app_1.views.error_404'
# 500 internal server error
# handler500 = 'app_1.views.error_500'
# # 400 bad request error
# handler400 = 'app_1.views.error_400'
# # 403 permission denied error
# handler403 = 'app_1.views.error_403'