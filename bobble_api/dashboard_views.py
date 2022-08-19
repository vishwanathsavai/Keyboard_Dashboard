'''
*	File Name	views.py
*	Created By	Vishwanath P
*	Reviewed By Rajeeva B
*	Description	About the files
    The functions which gets called for login,forgot password,validate OTP,New Password and Sign up
*	Version	1his is the original views script which gets created by Django
    This script has t
*	Sl No	Author	        Reviewer	Date	    Version	 Changes
*	1	    Vishwanath P	Rajeeva B	15/Aug/22	0.1	     Initial Draft
'''
#headers
import json
from . import database_connect
from django.http import HttpResponse
from .serializers import *

db_rs = database_connect.RS_DBConnection()
db_run = database_connect.DBConnection() #object of the class is created which will do all the operations over the DB
def Common_Dashboard(request):
    if request.method == "GET":  # Works on GET request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        token = body["token"]
        query = '''SELECT * from usrmeta u where c_usrmta_rst_tkn = "'''+token+'''";'''
        print(query)
        # token = database_connect.RunQuery(query)
        token = db_run.fetch(sql=query)
        if len(token) == 0:  # Invalid message sent
            result = {
                "code": 1,
                "msg":
                    "Invalid Credentials Provided"
            }
            # logger.log('Invalid Credentials Provided', phone)
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            user_token = token[0][0]
            print(user_token)
            if (user_token) > 5:  # Proper validation of user id and password
                query = "select app_sector from bobble_data_intelligence.v1_market_intelligence_aggregated_sector_apps vmiasa  "
                result = db_rs.fetch(query)
                # app_name

                str_input = '''{
                 "code" : "1",
                 "msg" : "",
                 "data" : {
                 "sectors" : ['''

                final_str = ''
                count = 0
                count_sec = 0
                for i in range(0, len(result)):
                    print(i, result[i][0])
                    if result[i][0] != '':
                        count_sec += 1
                        str_sample = '''{
                     "name" : "EX_SECTOR",
                     "value" : "SECTOR_COUNT",
                     "brands":['''
                        str_brand = '''{
                     "name" : "EX_BRAND",
                     "value": "BRAND_COUNT"
                     },'''
                        str_end = ''']
                     },'''
                        str_sample1 = str_sample.replace("EX_SECTOR", result[i][0]).replace('SECTOR_COUNT',
                                                                                            str(count_sec))
                        final_str += str_sample1
                        query_brand = "select app_name  from bobble_data_intelligence.v1_market_intelligence_aggregated_sector_apps vmiasa where app_sector = '" + \
                                      result[i][0] + "'"
                        result_val = db_rs.fetch(query_brand)
                        # print(str_sample1)
                        for j in result_val:
                            count += 1
                            str_brand1 = str_brand.replace('EX_BRAND', j[0]).replace('BRAND_COUNT', str(count))
                            # print(str_brand1)
                            final_str += str_brand1
                        final_str = final_str[:-1] + str_end
                        # final_str+=str_end

                final_str = str_input + final_str[:-1] + ''']
                 },
                 "token" : "TOKEN"
                }'''
                #token = "123456"
                final_str = final_str.replace("TOKEN", str(user_token))
                # print(final_str)
                final_json = eval(final_str)
                print(final_json)
                return HttpResponse(json.dumps(final_json), content_type='application/json')
            elif len(user_token) < 5 :  # blocked user check
                result = {
                    "code": 2,
                    "msg": "Login again!"
                }

                return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":  # For POST request its just printing the input request back
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')


def Dashboard_details(request):
    if request.method == "GET":#Works on GET Request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        token = body["token"]
        sector = body["data"]["sector"]
        brand = body["data"]["brand"]
        start_tm = body["data"]["time"]["start"]
        end_tm = body["data"]["time"]["end"]
        country = body["data"]["country"]
        print(token,sector,brand,start_tm,end_tm,country)
        query = '''SELECT u.c_usrinf_fn  from userinfo u ,usrmeta u2 where u.n_usrinf_usr_id  = u2.n_usrmta_usr_id and u2.c_usrmta_rst_tkn ="'''+token+'''"'''
        print(query)
        #token = database_connect.RunQuery(query)
        fname = db_run.fetch(query)
        print("FNAME",fname)
        try:
            if len(fname[0][0])==0:#Invalid token validation
                result = {
                        "code": 1,
                        "msg":
                            "Token Not Available"
                    }
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                first_str = '''{
                     "code" : "1",
                     "msg" : "Charts visible for the user",
                     "data" : {
                     "title":[{
                     "type" : "Title",
                     "value" : "Welcome! FIRSTNAME"
                     },{
                     "type" : "Subtitle",
                     "value": "Last updated on DD MMM YYYY."
                     }],
                     "charts":{
                     "0" :{
                     "title" : "",
                     "data" : [{
                     "title" : "Installed Users",
                     "description" : "List of users who have installed the selected application",
                     "cta" : "/mi/dashboard/instlUsr"
                     },{
                     "title" : "Active Users",
                     "description" : "List of users who are Active",
                     "cta" : "/mi/dashboard/actvUsr"
                     },{
                     "title" : "Open Rate",
                     "description" : "Description about open rate.",
                     "cta" : "/mi/dashboard/opnRt"
                     },{
                     "title" : "Sessions/Users",
                     "description" : "Description about open rate.",
                     "cta" : "/mi/dashboard/sesUsr"
                     },{
                     "title" : "Time Spent",
                     "description" : "Description about Time Spent.",
                     "cta" : "/mi/dashboard/tmSpnt"
                     }]
                     },
                     "1":{
                     "title" : "Sector Wise Data",
                     "data":[{
                     "title" : "",
                     "cta": "/mi/dashboard/sectrDt"
                     }]
                     },
                     "2":{
                     "title" : "People Insights",
                     "data":[{
                     "title" : "gender",
                     "description" : "Description about Time Spent.",
                     "cta": "/mi/dashboard/gender"
                     },{
                     "title" : "Age group by Gender",
                     "description" : "Description about Age group by Gender.",
                     "cta": "/mi/dashboard/agByGndr"
                     },{
                     "title" : "Income by age",
                     "description" : "Description about Income by age.",
                     "cta": "/mi/dashboard/incmByAg"
                     },{
                     "title" : "Region Wise Breakup",
                     "description" : "Description about Region wise breakup.",
                     "cta": "/mi/dashboard/regnWseBrkUp"
                     },{
                     "title" : "Searches",
                     "description" : "Description about Searches.",
                     "cta": "/mi/dashboard/dashSrchs"
                     },{
                     "title" : "Interests",
                     "description" : "Description about Interests.",
                     "cta": "/mi/dashboard/dashIntrsts"
                     },{
                     "title" : "Top Apps",
                     "description" : "Description about Top Apps.",
                     "cta": "/mi/dashboard/tpApps"
                     }]
                     }
                     }
                     },
                     "token" : "TOKEN"
                    }'''

                fname_query = '''SELECT u.c_usrinf_fn  from userinfo u ,usrmeta u2 where u.n_usrinf_usr_id  = u2.n_usrmta_usr_id and u2.c_usrmta_rst_tkn ="''' + str(
                    token) + '''"'''
                fname = db_run.fetch(fname_query)
                # print(fname)
                first_str = first_str.replace("FIRSTNAME", fname[0][0])
                final_json = eval(first_str)
                #print(final_json)

                return HttpResponse(json.dumps(final_json), content_type='application/json')
        except:
            result = {
                "code": 2,
                "msg":
                    "Login again!"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')

    elif request.method == "POST":#For POST it just prints back the input as output
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')


def Dashboard_InstrUsr(request):
    pass