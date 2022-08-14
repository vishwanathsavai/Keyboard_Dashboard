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
from . import supervisor_views
from . import venue_manager_views
from . import umpire_views
from . import customer_portal_view
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
    #path('sc/signupInit',views.SignupInit),
    path('sc/sup/login',supervisor_views.Sup_Login),
    path('sc/sup/forgot',supervisor_views.Sup_forgot_password),
    path('sc/sup/otp',supervisor_views.Sup_validate_OTP),
    path('sc/sup/pwd',supervisor_views.Sup_New_Password),
    path('sc/ump/login',umpire_views.ump_login),
    path('sc/ump/otp',umpire_views.ump_validate_OTP),
    path('sc/adm/login',venue_manager_views.vm_login),
    path('sc/adm/forgot',venue_manager_views.vm_forgot_password),
    path('sc/adm/otp',venue_manager_views.vm_validate_OTP),
    path('sc/logout',customer_portal_view.logout_customer),
    path('sc/nav',customer_portal_view.Customer_Navigation),
    path('sc/notify',customer_portal_view.Customer_Notify),#pending
    path('sc/dash',customer_portal_view.Customer_Dash),#pending
    path('sc/booking/list',customer_portal_view.Customer_Booking_list),
    path('sc/booking/search',customer_portal_view.Booking_Search),
    path('sc/leader',customer_portal_view.Leader_Stats)
]