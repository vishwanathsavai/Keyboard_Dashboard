'''
*	File Name	urls.py
*	Created By	Vishwanath P
*	Reviewed By
*	Description	About the files
    This is a sub urls.py script which gets created when a project is created
    Here we are calling all the links which in-trun will call the functions which will handle the API requests
*	Version	1
*	Sl No	Author	        Reviewer	Date	    Version	 Changes
*	1	    Vishwanath P	Rajeeva B	01/Jul/22	0.1	     Initial Draft
'''
from . import views
import Django_Script

from django.contrib import admin
from django.urls import path

#List of all the links which can be used
urlpatterns = [
    path('admin/', admin.site.urls),
    path('mi/login',views.login),
    path('mi/forgot',views.forgot_password),
    path('mi/validateFrgt',views.validate_Frgt),
    path('mi/newPwd',views.New_Password),
    path('mi/signup',views.SignupInit),
    path('mi/sendOTP',views.SendOTP),
    path('mi/sendEmailOTP',views.SendEmailOTP),
    #path('sc/signupInit',views.SignupInit)
]
