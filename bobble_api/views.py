'''
*	File Name	views.py
*	Created By	Vishwanath P
*	Reviewed By Rajeeva B
*	Description	About the files
    The functions which gets called for login,forgot password,validate OTP,New Password and Sign up
*	Version	1his is the original views script which gets created by Django
    This script has t
*	Sl No	Author	        Reviewer	Date	    Version	 Changes
*	1	    Vishwanath P	Rajeeva B	01/Jul/22	0.1	     Initial Draft
'''
#headers
import json
from . import database_connect
from django.http import HttpResponse
from .serializers import *


db_run = database_connect.DBConnection() #object of the class is created which will do all the operations over the DB
#login validation script
def login(request):
        if request.method == "GET":#Works on GET request
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print(body)
            email = body["uid"]
            password = body["pwd"]
            remember = body["remember"]
            if remember == 0 or remember == 1:
                query = '''UPDATE bobble.usrmeta SET  b_usrmta_rmbr_me=0 where n_usrmta_usr_id in (select n_usrinf_usr_id from userinfo where c_usrinf_eml="'''+ email +'''");'''
                print(query)
                # token = database_connect.RunQuery(query)
                token = db_run.fetch(sql=query)

            if '@' in email:
                #query for the input data validation
                query = '''select u.c_usrmta_rst_tkn ,u2.b_usr_blk  from bobble.usrmeta u ,bobble.user u2 ,bobble.userinfo u3  where u3.c_usrinf_eml = "'''+ email +'''" and u3.c_usrinf_pwd ="'''+ password +'''" and u3.n_usrinf_usr_id = u2.n_usr_id and u2.n_usr_id = u.n_usrmta_usr_id ;'''
                print(query)
                #token = database_connect.RunQuery(query)
                token = db_run.fetch(sql=query)
            else:
                # query for the input data validation
                query = '''select u.c_usrmta_rst_tkn ,u2.b_usr_blk  from bobble.usrmeta u ,bobble.user u2 ,bobble.userinfo u3  where u3.c_usrinf_ph = "'''+ email +'''" and u3.c_usrinf_pwd ="'''+ password +'''" and u3.n_usrinf_usr_id = u2.n_usr_id and u2.n_usr_id = u.n_usrmta_usr_id ;'''
                print(query)
                # token = database_connect.RunQuery(query)
                token = db_run.fetch(sql=query)
            if len(token) == 0:#Invalid message sent
                result = {
                "code": 1,
                "msg":
                "Invalid Credentials Provided"
            }
                #logger.log('Invalid Credentials Provided', phone)
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                user_token = token[0][0]
                user_blocked = token[0][1]
                print(user_token,user_blocked)
                if len(user_token) > 5 and user_blocked==0:#Proper validation of user id and password
                    result = {
                                "code": 1,
                                "msg": "Login Successful",
                                "data": {
                                    "token": user_token
                                }
                            }
                    print(result)
                    return HttpResponse(json.dumps(result), content_type='application/json')
                elif len(user_token) > 5 and user_blocked==1:#blocked user check
                    result = {
                             "code" : 1,
                             "msg"  : "You have been Blocked!"
                            }

                    return HttpResponse(json.dumps(result), content_type='application/json')
        elif request.method == "POST":#For POST request its just printing the input request back
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print(body)
            return HttpResponse(json.dumps(body), content_type='application/json')

#Forgot password function validation
def forgot_password(request):
    if request.method == "GET":#Works on GET Request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        email = body["uid"]
        query = '''select u.c_usrmta_rst_tkn ,u2.b_usr_blk  from usrmeta u ,`user` u2 ,userinfo u3 where u3.c_usrinf_eml = "'''+ email +'''" and u3.c_usrinf_pwd ="'''+ password +'''" and u3.n_usrinf_usr_id = u2.n_usr_id and u2.n_usr_id = u.n_usrmta_usr_id ;'''
        print(query)
        #token = database_connect.RunQuery(query)
        token = db_run.fetch(query)
        if len(token)==0:#Invalid token validation
            result = {
                    "code": 1,
                    "msg":
                        "Token Not Available"
                }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            user_token = token[0]['n_usrmta_token']
            user_blocked = token[0]['b_usr_blckd']
            if len(user_token) > 5 and user_blocked == 0:#When the script receives valid input this function kicks in
                result = {
     "code" : 1,
     "msg"  : "Please check the E-Mail sent to your account!"
    }

                return HttpResponse(json.dumps(result), content_type='application/json')
            elif len(user_token) > 5 and user_token == 1:#checking for blocked user
                result = {
                    "code": 1,
                    "msg": "You have been Blocked!"
                }

                return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":#For POST it just prints back the input as output
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def validate_Frgt(request):
    #OTP validation function
    if request.method == "GET":#Works on GET request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)

        resend = 0
        try:#exception handling
            #phone = body["uid"]
            token = body["token"]
            query = '''select u.c_usrmta_rst_tkn from usrmeta u where u.c_usrmta_rst_tkn = "'''+token+''''''
            print(query)
            #token = database_connect.RunQuery(query)
            token = db_run.fetch(query)
            resend = body["resend"]
            if resend == 1:#resends checks
                if len(token)==0:#when the limit for resend is met this message is sent
                    result = {
                             "code" : 2,
                             "msg"  : "Invalid Link has been clicked! Please check again"
                            }

                    return HttpResponse(json.dumps(result), content_type='application/json')
                elif len(token[0][0]) > 5:#Valid OTP when checked this is sent back
                    result = {
                             "code" : 1,
                             "msg" : "Please enter your new password",
                             "data" :{
                              "token" : token[0][0]
                             }
                            }


                    return HttpResponse(json.dumps(result), content_type='application/json')
                elif len(token[0][0]) > 5 and token[0][1] == 1:#check for blocked user
                    result = {
                        "code": 1,
                        "msg": "You have been Blocked!"
                    }

                    return HttpResponse(json.dumps(result), content_type='application/json')
        except KeyError:#When Keyerror occurs this message is printed
            phone = body["uid"]
            otp = str(body["otp"])
            token = body["token"]
            query = '''select u2.n_usrmta_token  from users u , usrmta u2 where u.c_usr_ph = "''' + phone + '''" and u.n_usr_rl_id =1 and u.n_usr_id = u2.n_usrmta_usr_id  and u2.n_usrmta_otp_nd = ''' + otp + ''' and u2.n_usrmta_token ="''' + token + '''";'''
            print(query)
            token = database_connect.RunQuery(query)
            if len(token)==0:#Check for invalid OTP
                result = {
                         "code" : 2,
                         "msg"  : "OTP Invalid, Please enter again"
                        }

                return HttpResponse(json.dumps(result), content_type='application/json')
            elif len(token[0][0]) > 5:#When OTP is valid
                result = {
                         "code" : 1,
                         "msg" : "Please enter your new password",
                         "data" :{
                          "token" : token[0][0]
                         }
                        }


                return HttpResponse(json.dumps(result), content_type='application/json')
            elif len(token[0][0]) > 5 and token[0][1] == 1:#When OTP is valid but its fr a blocked user
                result = {
                    "code": 1,
                    "msg": "You have been Blocked!"
                }

                return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":#POST request check
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def New_Password(request):
    #Validation for NEw password
    if request.method == "POST":#This works on POST Request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        phone = body["uid"]
        pwd = body["pwd"]
        token = body["token"]
        #query = '''update users set c_usr_pwd = "'''+pwd+'''" where c_usr_ph = "'''+phone+'''" and u.n_usr_rl_id =1 and n_usr_id in (select n_usrmta_usr_id from usrmta where n_usrmta_token = "'''+token+'''");'''
        query = '''UPDATE bobble.userinfo SET  c_usrinf_pwd=""'''+pwd+'''" where n_usrinf_usr_id in (select u2.n_usrmta_usr_id from usrmeta u2 where u2.c_usrmta_rst_tkn = "'''+token+'''");'''
        print(query)
        token = database_connect.RunQuery(query)
        print(token)

        result = {
                 "code" : 1,
                 "msg"  : "Password Changed! Please login Again"
                }

        return HttpResponse(json.dumps(result), content_type='application/json')

    elif request.method == "GET":#for GET it just prints the data
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')


def generate_access_token():
    #Generates access token in random
    import random, string
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=13))
    return x


def Signup(request):
    #Sign up check is handled for phone input
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        phone = body["phone"]
        access_token = generate_access_token()

        result = {
                 "code" : 1,
                 "msg"  : "Please complete your profile!",
                 "data"  :{
                  "token" : generate_access_token(),#random gen function is called
                 "filledSet": {"name": "phone_number", "value": phone}
                 }
                }


        return HttpResponse(json.dumps(result), content_type='application/json')

    elif request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def SignupInit(request):
    #Sign up initialisation function
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        #Gets all the values from input payload
        fname = body["fname"]
        lname = body["lname"]
        company = body["company"]
        desg = body["desg"]
        phone = body["phone"]
        email = body["email"]
        pwd = body["password"]
        otpEmail = body["otpEMail"]
        otpPh = body["otpPh"]
        access_token = generate_access_token()#generate access token function is called

        query = '''select (select sysdate() from dual) as sys_date ,max(n_usr_id) as 'max_val' from bobble.user u ;'''
        result = db_run.fetch(query)
        user_id = result[0][1]
        system_dt = result[0][0]
        query = '''INSERT INTO bobble.`user`
(n_usr_id, b_usr_del, b_usr_blk, b_usr_dactv, dt_usr_crtd_on, n_usr_rl_id, b_usr_pwd_rst)
VALUES('''+str(user_id+1)+''', 0, 0, 0, "'''+str(system_dt)+'''", 1, 0);'''
        print(query)
        db_run.fetch(query)
        query_insert = '''INSERT INTO bobble.userinfo
( n_usrinf_usr_id, c_usrinf_eml, c_usrinf_pwd, c_usrinf_fn, c_usrinf_ln, c_usrinf_des, c_usrinf_ph, c_usrinf_cmp)
VALUES('''+str(user_id+1)+''', "'''+str(email)+'''", "'''+str(pwd)+'''", "'''+str(fname)+'''", "'''+str(lname)+'''", "'''+str(desg)+'''", "'''+str(phone)+'''", "'''+str(company)+'''");'''
        db_run.fetch(query_insert)
        token_generated = generate_access_token()
        query_usrmeta = '''INSERT INTO bobble.usrmeta
( n_usrmta_usr_id, c_usrmta_iwt, c_usrmta_oauth, dt_usrmta_lst_rst_lnk, c_usrmta_rst_tkn, b_usrmta_apprvd, b_usrmta_ph_appvd, dt_usrmta_lgn, b_usrmta_rmbr_me)
VALUES( '''+str(user_id+1)+''', 'jwt_2', 'oauth_2', "'''+str(system_dt)+'''", "'''+token_generated+'''", 1, 1, "'''+str(system_dt)+'''", 1);'''
        db_run.fetch(query_usrmeta)
        #Insert Query is missing
        result = {
                 "code" : 1,
                 "msg"  : "Signup successful! Please login again",
                }



        return HttpResponse(json.dumps(result), content_type='application/json')

    elif request.method == "GET":#GEt will just print the input value
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def SendOTP(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        phone = str(body["phone"])
        #password = body["pwd"]
        query = '''select u.c_usrinf_ph from userinfo u where u.c_usrinf_ph = "'''+phone+'''";'''
        print(query)
        valid_phone = db_run.fetch(query)

        if len(valid_phone[0]) == 0:
            result = {
                "code": 2,
                "msg":
                    "Please Check the details entered!"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif len(valid_phone[0]['c_usrinf_ph']) > 5 :
            result = {
                "code": 1,
                "msg": "Signup successful! Please login again",
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')


def SendEmailOTP(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        phone = str(body["uid"])
        #password = body["pwd"]
        query = '''select u.c_usrinf_ph from userinfo u where u.c_usrinf_ph = "'''+phone+'''";'''
        print(query)
        valid_phone = db_run.fetch(query)

        if len(valid_phone[0]) == 0:
            result = {
                "code": 2,
                "msg":
                    "Please Check the details entered!"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif len(valid_phone[0][0]) > 5 :
            result = {
                "code": 1,
                "msg": "Signup successful! Please login again",
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')