# views.py
import json
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import render,redirect
from . import database_connect
from .serializers import *





def Sup_Login(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        phone = str(body["uid"])
        password = body["pwd"]
        query = '''select u2.n_usrmta_token,u.b_usr_blckd   from users u , usrmta u2 where u.c_usr_ph = "''' + phone + '''" and u.n_usr_rl_id =3 and u.c_usr_pwd = "''' + password + '''" and u.n_usr_id = u2.n_usrmta_usr_id  ;'''
        print(query)
        token = database_connect.RunQuery(query)

        if len(token) == 0:
            result = {
                "code": 1,
                "msg":
                    "Invalid Credentials Provided"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif len(token[0][0]) > 5 and token[0][1] == 0:
            result = {
                "code": 1,
                "msg": "Login Successful",
                "data": {
                    "token": token[0][0]
                }
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif len(token[0][0]) > 5 and token[0][1] == 1:
            result = {
                "code": 1,
                "msg": "You have been Blocked!"
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')


def Sup_forgot_password(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        phone = str(body["uid"])
        query = '''select u2.n_usrmta_token,u.b_usr_blckd   from users u , usrmta u2 where u.c_usr_ph = "''' + phone + '''" and u.n_usr_rl_id =3 and u.n_usr_id = u2.n_usrmta_usr_id  ;'''
        print(query)
        token = database_connect.RunQuery(query)
        if len(token) == 0:
            result = {
                "code": 1,
                "msg":
                    "Token Not Available"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif len(token[0][0]) > 5 and token[0][1] == 0:
            result = {
                "code": 1,
                "msg": "Please enter the OTP sent to your account",
                "data": {
                    "token": token[0][0]
                }
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
        elif len(token[0][0]) > 5 and token[0][1] == 1:
            result = {
                "code": 1,
                "msg": "You have been Blocked!"
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')


def Sup_validate_OTP(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)

        resend = 0
        try:
            phone = body["uid"]
            token = body["token"]
            query = '''select u2.n_usrmta_token  from users u , usrmta u2 where u.c_usr_ph = "''' + phone + '''" and u.n_usr_rl_id =3 and u.n_usr_id = u2.n_usrmta_usr_id  and u2.n_usrmta_token ="''' + token + '''";'''
            print(query)
            token = database_connect.RunQuery(query)
            resend = body["resend"]
            if resend == 1:
                if len(token)==0:
                    result = {
                             "code" : 2,
                             "msg"  : "You have reached the maximum number of times an OTP can be sent to this number, please try again after sometime"
                            }

                    return HttpResponse(json.dumps(result), content_type='application/json')
                elif len(token[0][0]) > 5:
                    result = {
                             "code" : 1,
                             "msg" : "Please enter your new password",
                             "data" :{
                              "token" : token[0][0]
                             }
                            }


                    return HttpResponse(json.dumps(result), content_type='application/json')
                elif len(token[0][0]) > 5 and token[0][1] == 1:
                    result = {
                        "code": 1,
                        "msg": "You have been Blocked!"
                    }

                    return HttpResponse(json.dumps(result), content_type='application/json')
        except KeyError:
            phone = body["uid"]
            otp = str(body["otp"])
            token = body["token"]
            query = '''select u2.n_usrmta_token  from users u , usrmta u2 where u.c_usr_ph = "''' + phone + '''" and u.n_usr_rl_id =3 and u.n_usr_id = u2.n_usrmta_usr_id  and u2.n_usrmta_otp_nd = ''' + otp + ''' and u2.n_usrmta_token ="''' + token + '''";'''
            print(query)
            token = database_connect.RunQuery(query)
            if len(token)==0:
                result = {
                         "code" : 2,
                         "msg"  : "OTP Invalid, Please enter again"
                        }

                return HttpResponse(json.dumps(result), content_type='application/json')
            elif len(token[0][0]) > 5:
                result = {
                         "code" : 1,
                         "msg" : "Please enter your new password",
                         "data" :{
                          "token" : token[0][0]
                         }
                        }


                return HttpResponse(json.dumps(result), content_type='application/json')
            elif len(token[0][0]) > 5 and token[0][1] == 1:
                result = {
                    "code": 1,
                    "msg": "You have been Blocked!"
                }

                return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def Sup_New_Password(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        phone = body["uid"]
        pwd = body["pwd"]
        token = body["token"]
        query = '''update users set c_usr_pwd = "'''+pwd+'''" where c_usr_ph = "'''+phone+'''" and u.n_usr_rl_id =3 and n_usr_id in (select n_usrmta_usr_id from usrmta where n_usrmta_token = "'''+token+'''");'''
        print(query)
        token = database_connect.RunQuery(query)
        print(token)

        result = {
                 "code" : 1,
                 "msg"  : "Password Changed! Please login Again"
                }

        return HttpResponse(json.dumps(result), content_type='application/json')

    elif request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')