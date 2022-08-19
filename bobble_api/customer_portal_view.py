'''
*	File Name	customer_portal_view.py
*	Created By	Vishwanath P
*	Reviewed By
*	Description	About the files
    This script has all the functions related to customer portal. When the API is hit it gets redirected
    to this script where the particular function is called and data gets fetched and returned back
*	Version	1
*	Sl No	Author	        Reviewer	Date	    Version	 Changes
*	1	    Vishwanath P	Rajeeva B	01/Jul/22	0.1	     Initial Draft
'''

import json
from . import database_connect
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

from .serializers import *


def logout_customer(request):
    '''
    This function is to get the token and log out the customer
    '''
    if request.method == "GET":#Expecting the function to give proper response for GET
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        token = body["token"]
        query = '''select count(1) from usrmta u where u.n_usrmta_token = "'''+token+'''";'''
        print(query)
        result = database_connect.RunQuery(query)
        if result[0][0]==1:#if the token is right then this checks in
            result = {
                        "code" : 1,
                        "msg" : "Logged out successfully"
                    }
            # logger.log('Invalid Credentials Provided', phone)
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif result[0][0] == 0:#if token is not proper then Logout fails
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:#Any other value is handled here
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":#For the POST request it just prints the input request itself.
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def Customer_Navigation(request):
    #Sends Customer navigation details
    if request.method == "GET":#Works on GET function
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        token = body["token"]
        query = '''select count(1) from usrmta u where u.n_usrmta_token = "''' + token + '''";'''
        print(query)
        result = database_connect.RunQuery(query)
        if result[0][0] == 1:#For Valid Token
            query_icon = ''' select c_nvw_nm,c_nvw_lnk from nav_web nw ;'''

            icon_result = database_connect.RunQuery(query_icon)
            json_string = '''{
             "code" : 1,
             "item" : {'''
            link_string = ''''''
            sub_string = '''"range_val" : {
                          "name": "First_change",
                          "icon": "icon.svg",
                          "redirect": "page_link"
                          },'''
            for i in range(0, len(icon_result)):
                changed_str = sub_string.replace('range_val', str(i)).replace('First_change',
                                                                              icon_result[i][0]).replace('page_link',
                                                                                                         icon_result[i][
                                                                                                             1])
                link_string += changed_str
            result = json_string+link_string+'''},
             "logo": {
              "alt": "SC Logo",
              "path": "http://sportcenter.com/images/logo.png"
             }
            }'''
            result =eval (result)
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif result[0][0] == 0:#Invalid Token
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":#For post request it just sends back payload info
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def Customer_Notify(request):
    '''This is for Customer notification functionality
        4 different codes had to be handled which are don in the below try catch and else if ladder'''
    try:#Exception handling
        if request.method == "GET":#Works on GET
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print(body)
            token = body["token"]
            query = '''select count(1) from usrmta u where u.n_usrmta_token = "''' + token + '''";'''
            print(query)
            result = database_connect.RunQuery(query)
            if result[0][0] == 1:#Valid token and code 1
                result = {
                         "code" : "1",
                         "data":{
                          "0" : {
                           "title" : "This is a notification",
                           "description" : "You have been invited to view this notification and take some action for it",
                           "cta" : "link"
                          },
                          "1":{
                           "title" : "This is a notification",
                           "description" : "you have been just asked to view this notification and not take any action for it",
                          }
                         }
                        }
                # logger.log('Invalid Credentials Provided', phone)
                return HttpResponse(json.dumps(result), content_type='application/json')
            elif result[0][0] == 0:
                result = {
                         "code" : 2,
                         "msg": "Please check the selected item, if issue persists contact admin"
                        }
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result = {
                         "code" : 3,
                         "msg": "Please login again",
                         "redirect": "/home"
                        }

                return HttpResponse(json.dumps(result), content_type='application/json')
        elif request.method == "POST":
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print(body)
            return HttpResponse(json.dumps(body), content_type='application/json')
    except SystemError:
        if request.method == "GET":
                result = {
                         "code" : 0,
                         "msg": "Server error! Please check your connection, if issue persists contact admin"
                        }
                # logger.log('Invalid Credentials Provided', phone)
                return HttpResponse(json.dumps(result), content_type='application/json')
        elif request.method == "POST":
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print(body)
            return HttpResponse(json.dumps(body), content_type='application/json')

def dashboard_all(token,ball_str):
    db_obj = database_connect.DBConnection()
    # Name Fetch
    name_query = '''select CONCAT(c_usrinfo_frst_nm,' ',c_usrinfo_lst_nm) as 'Full_Name' from userinfo u WHERE n_usrinfo_usr_id in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    name = db_obj.fetch(name_query.replace('TOKEN_KEY', token))[0]['Full_Name']
    # print(name)
    # Title Fetch
    title_query = '''select c_usrinfo_prfl_sub  as 'Title' from userinfo u WHERE n_usrinfo_usr_id in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    title = db_obj.fetch(title_query.replace('TOKEN_KEY', token))[0]['Title']
    # print(title)
    # Total Matches
    matches_query = '''select count(DISTINCT n_inn_mtch_id) as 'matches' from innings i where n_inn_id in
    (select n_ovrs_inn_id  from overs o where n_ovrs_id in
    (select n_bls_ovrs_id  from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and ( bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    or  bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'))));'''
    #print(matches_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))
    matches_total = db_obj.fetch(matches_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['matches']
    # print(matches_total)
    # Total_runs
    runs_query = '''select sum(n_bls_run) as 'runs' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and (   bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'));'''
    total_runs = db_obj.fetch(runs_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['runs']
    # print(total_runs)
    # total wkts
    wkts_query = '''select count(1) as 'wkts' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and n_bls_wkt_typ in (1,2,4,7);'''
    total_wkts = db_obj.fetch(wkts_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['wkts']
    # print(total_wkts)
    # total catches
    catches_query = '''select count(1) as 'catches' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_wkt_ass_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and n_bls_wkt_typ = 4;'''
    total_Catches = db_obj.fetch(catches_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['catches']
    # print(total_Catches)
    # Total Stumpings
    stumpings_total = '''select count(1) as 'stumpings' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_wkt_ass_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and n_bls_wkt_typ  = 3;'''
    total_stumps = db_obj.fetch(stumpings_total.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['stumpings']
    # print(total_stumps)
    strike_rate_query = '''select (sum(bs.n_bls_run)/COUNT(bs.n_bls_id))*100 as 'strike rate'  from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    sr_total = db_obj.fetch(strike_rate_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['strike rate']
    # print(sr_total)
    eco_query = '''select (sum(bs.n_bls_run)/(COUNT(bs.n_bls_id)/6)) as 'Economy'  from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    eco_total = db_obj.fetch(eco_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['Economy']
    # print(eco_total)
    highest_runs_query = '''select max(n_bls_run) as 'highest_runs' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and (bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'));'''
    high_runs = db_obj.fetch(highest_runs_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))[0]['highest_runs']
    # print(high_runs)

    # match full info
    match_info_list = []
    first4_query = '''SELECT bt.c_bltyp_nm ,m.n_mtch_id, m.dt_mtch_strt,v.c_vn_nm  from `match` m ,ball_type bt  ,venue v,innings i  ,ball_summary bs ,overs o where
    bt.n_blyp_id  in (BALL_TYPE) and
    bs.n_bls_ovrs_id = o.n_ovrs_id AND
    o.n_ovrs_inn_id = i.n_inn_id AND
    i.n_inn_mtch_id = m.n_mtch_id AND
    m.n_mtch_vn_id = v.n_vn_id AND
    ( bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    or  bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'))
    GROUP by bt.c_bltyp_nm ,m.n_mtch_id order by m.n_mtch_id ;'''
    first4_data = db_obj.fetch(first4_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))
    # print(first4_data)
    match_info_list.extend(first4_data)
    second_set_query = '''select bs.bs_mtch_id,sum(n_bls_run),(sum(bs.n_bls_run)/COUNT(bs.n_bls_id))*100 as 'strike rate',max(n_bls_run),t.c_tm_nm  from ball_summary bs ,team_members tm ,teams t where 
    bs.bs_bll_typ in (BALL_TYPE) and
    bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and tm.n_tmb_usr_id = bs.n_bls_btsm_id
    and t.n_tm_id = tm.n_tmb_tm_id
    GROUP by bs.bs_mtch_id,t.c_tm_nm order by bs.bs_mtch_id;'''
    second_set_data = db_obj.fetch(second_set_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))
    # print(second_set_data)
    match_info_list.extend(second_set_data)
    third_query = '''select bs_mtch_id,mr.c_mrs_res ,t.c_tm_nm  from match_result mr ,ball_summary bs,teams t
    where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and mr.n_mrs_mtch_id = bs.bs_mtch_id and mr.n_mrs_wn_tm_id = t.n_tm_id group by bs_mtch_id,mr.c_mrs_res ,t.c_tm_nm ;'''
    third_data = db_obj.fetch(third_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))
    # print(third_data)
    match_info_list.extend(third_data)
    fourth_set = '''select n_mtch_id ,(select t.c_tm_nm  from teams t where t.n_tm_id = m.n_mtch_tma_id) as 'team name A' ,
    (select t.c_tm_nm  from teams t where t.n_tm_id = m.n_mtch_tmb_id) as 'team name B'
    from `match` m , ball_summary bs  where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'ALAJCOAMKDSLC')
    and bs.bs_mtch_id = m.n_mtch_id GROUP by n_mtch_id ,n_mtch_tma_id ,n_mtch_tmb_id order by m.n_mtch_id;'''
    fourth_data = db_obj.fetch(fourth_set.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))
    # print(fourth_data)
    match_info_list.extend(fourth_data)
    fifth_query = '''select bs.bs_mtch_id,sum(n_bls_run),tm.n_tmb_usr_id,(select count(1) as 'wkts'  from ball_summary bss where bss.n_bls_bwlr_id = tm.n_tmb_usr_id and n_bls_wkt_typ in (1,2,4,7)) as 'wkts' ,
    (select count(1) as 'catches' from ball_summary bs where bs.n_bls_wkt_ass_id  = tm.n_tmb_usr_id and  n_bls_wkt_typ = 4) as 'catches' ,
    (select count(1) as 'stumpings' from ball_summary bs where bs.n_bls_wkt_ass_id = tm.n_tmb_usr_id and  n_bls_wkt_typ = 3) as 'stumpings' ,
    (sum(bs.n_bls_run)/(COUNT(bs.n_bls_id)/6)) as 'Economy',t.c_tm_nm  from ball_summary bs ,team_members tm ,teams t where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and tm.n_tmb_usr_id = bs.n_bls_bwlr_id
    and t.n_tm_id = tm.n_tmb_tm_id
    GROUP by bs.bs_mtch_id,t.c_tm_nm,tm.n_tmb_usr_id  ;'''
    fifth_data = db_obj.fetch(fifth_query.replace('BALL_TYPE',ball_str).replace('TOKEN_KEY', token))
    # print(fifth_data)
    match_info_list.extend(fifth_data)
    match_json = '''"LOOP_VAL" : {
        "ball_type" : "BALL_TYPE",
        "team" : ["TEAMA","TEAMB"],
        "id" : "CRIC1234",
        "date" : "MATCH_DATE",
        "venue": {
         "name" : "VENUE_NAME",
         "link" : "/venue/id/1234"
        },
        "player_team": "PLAYERS_TEAM",
        "player_statistics":{
         "matches" : "LOOP_VAL",
         "runs"  : "MATCH_RUNS",
         "wickets" : "MATCH_WICKETS",
         "catches" : "MATCH_CATCHES",
         "stumpings" : "MATCH_STUMPS",
         "strike rate":"MATCH_SR",
         "Economy" : "MATCH_ECO",
         "highest" : "MATCH_SCORE"
        },
        "result" : {
         "team":"WINNING_TEAM",
         "stat":"WINNING_STATS"
        },
        "gallery" :{
         "0" : {
          "type": "vidoe",
          "link":"video.link",
         "1": {
          "type": "img",
          "link": "img.link"
         }
        }
       }
      },'''

    final_str = ''

    for i in range(0, matches_total):
        # print(i)
        replace_str = match_json.replace('LOOP_VAL', str(i)).replace('BALL_TYPE', first4_data[i]['c_bltyp_nm']).replace(
            'TEAMA', fourth_data[i]['team name A']).replace('TEAMB', fourth_data[i]['team name B']).replace(
            'MATCH_DATE', str(first4_data[i]['dt_mtch_strt'])).replace('VENUE_NAME', first4_data[i]['c_vn_nm']).replace(
            'PLAYERS_TEAM', second_set_data[i]['c_tm_nm']).replace('MATCH_RUNS',
                                                                   str(second_set_data[i]['sum(n_bls_run)']))
        replace_str = replace_str.replace('MATCH_WICKETS', str(fifth_data[i]['wkts'])).replace('MATCH_CATCHES', str(fifth_data[i]['catches'])).replace('MATCH_STUMPS', str(fifth_data[i]['stumpings'])).replace('MATCH_SR', str(second_set_data[i]['strike rate']))
        replace_str = replace_str.replace('MATCH_ECO', str(fifth_data[i]['Economy'])).replace('MATCH_SCORE', str(fifth_data[i]['sum(n_bls_run)'])).replace('WINNING_TEAM', third_data[i]['c_tm_nm']).replace('WINNING_STATS',third_data[i]['c_mrs_res'])
        final_str += replace_str

    # print(final_str[:-1])
    final_str = final_str[:-1] + '''
    }]
}
}
    '''
    first_half_json = '''{
     "code" : 1,
     "data": {
      "top" : {
       "name" : "PLAYER_NAME",
       "title": "PLAYER_TITLE"
      },
      "statistics":{
       "0":{
        "matches" : "PLAYER_MATCHES",
        "runs"  : "PLAYER_RUNS",
        "wickets" : "PLAYER_WICKETS",
        "catches" : "PLAYER_CTACHES",
        "stumpings" : "PLAYER_STUMPINGS",
        "strike rate":"PLAYER_SR",
        "Economy" : "PLAYER_ECO",
        "highest" : "PLAYER_HR"
       }
      },
      "matches" : [{
      '''

    first_json = first_half_json.replace('PLAYER_NAME', name).replace('PLAYER_TITLE', title).replace('PLAYER_MATCHES',
                                                                                                     str(
                                                                                                         matches_total)).replace(
        'PLAYER_RUNS', str(total_runs))
    first_json = first_json.replace('PLAYER_WICKETS', str(total_wkts)).replace('PLAYER_CTACHES',
                                                                               str(total_Catches)).replace(
        'PLAYER_STUMPINGS', str(total_stumps)).replace('PLAYER_SR', str(sr_total)).replace('PLAYER_ECO',
                                                                                           str(eco_total)).replace(
        'PLAYER_HR', str(high_runs))

    final_json = first_json + final_str
    print(final_json)
    #final_json = eval(final_json)
    return final_json
def Customer_Dash(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        token = body["token"]
        filter_flag = body["filter"]
        query = '''select count(1) from usrmta u where u.n_usrmta_token = "''' + token + '''";'''
        print(query)
        result = database_connect.RunQuery(query)
        if result[0][0] == 1:
            if filter_flag == 0:
                ball_str = '1,2'
                final_json1 = dashboard_all(token,ball_str)
                return HttpResponse(json.dumps(final_json1), content_type='application/json')
            elif filter_flag == 1:
                ball_str = '2'
                final_json1 = dashboard_all(token, ball_str)
                return HttpResponse(json.dumps(final_json1), content_type='application/json')
            elif filter_flag == 2:
                ball_str = '1'
                final_json1 = dashboard_all(token, ball_str)
                return HttpResponse(json.dumps(final_json1), content_type='application/json')
            else:
                result = {
                    "code": 1,
                    "msg": "Logged out successfully"
                }
                # logger.log('Invalid Credentials Provided', phone)
                return HttpResponse(json.dumps(result), content_type='application/json')
        elif result[0][0] == 0:
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')

def Booking_data_check(token,ball_type,range_val,match_status):
    db_obj = database_connect.DBConnection()

    first_str = '''{
     "code" : 1,
     "data": {
      "filter":{
       "min" : 1,
       "max" : RANGE_VAL
      },
      "search":{
       "url": "/sc/searchBooking",
       "min": "3"
      },
      "booking":{'''

    first_str = first_str.replace('RANGE_VAL', str(range_val))

    second_str = '''"COUNT" : {
    "id":"BOOKING_ID",
        "type":"MATCH_STATUS",
        "action_button":[{
         "type":"email",
         "action":"/sc/bookingmanage/match/BOOKING_ID"
        },{
         "type":"edit",
         "action":"/sc/bookingmanage/edit/BOOKING_ID"
        },{
         "type":"cancel",
         "action":"/sc/bookingmanage/can/BOOKING_ID"
        },{
         "type":"download",
         "action" : "/sc/booking/dwnld/BOOKING_ID"
        }],
        "top":{
         "bookingid":"BOOKING_ID",
         "bookingdate":"BOOKING_DATE",
         "bookingmail":"BOOKING_USER_EMAIL",
         "tranid":"TRANSACTION_ID",
         "billingdata":"BILLING_DATE",
         "contact":"BOOKING_USER_CONTACT",
         "bookinghrs":"BOOKING_HRS",
         "time":{
          "start":"BOOKING_START_TM",
          "end":"BOOKING_END_TIME"
         }
        },
        "mid":{
         "venue" : {
          "title" : "BOOKING_VENUE",
           "link" : "/venue/id/BOOKING_VENUE_ID"
         }
        },
        "bottom":{
         "facilities":[{
          "title" : "supervisor",
          "value" : "SUPERVISOR_NAME",
         },{
          "title" : "Ball Type",
          "value" : "BALL_TYPE"
         },{
          "title" : "Kit",
          "value" : "Standard"
         },{
          "title" : "Below 18",
          "Value" : "BELOW_AGE_FLAG"
         },{
          "title" : "Physically Disabled",
          "Value" : "PHY_DISABLE_FLAG"
         }]
        }
       },'''

    booking_query = '''select b.n_bk_id as 'bookingid',b.dt_bk_tmstmp as 'bookingdt',u.c_usr_eml ,u.c_usr_ph ,TIMEDIFF (b.t_bk_end,b.t_bk_strt) as 'bookinghrs',
    b.t_bk_strt ,b.t_bk_end , v.c_vn_nm ,v.n_vn_id as 'venue_id',(select CONCAT(u4.c_usrinfo_frst_nm,' ',u4.c_usrinfo_lst_nm) from users u3,userinfo u4  where u3.n_usr_id=b.n_bk_sup_id and u4.n_usrinfo_usr_id = u3.n_usr_id) as 'Supervisor_name',
    (select bt.c_bltyp_nm  from ball_type bt where bt.n_blyp_id = b.b_bk_bll_typ) as 'ball_type',b.b_bk_blw_age,
    (select ms2.c_mtchsts_nm  from match_status ms2 where ms2.n_mtchsts_id = b.n_bk_sts) as 'Match_Status'
    from booking b , booking_master bm , users u ,usrmta u2 ,venue v ,match_status ms WHERE
    u2.n_usrmta_id = u.n_usr_id AND
    u.n_usr_id = bm.n_bkm_usr AND
    b.n_bk_vn = v.n_vn_id AND
    bm.n_bkm_id = b.n_bk_bkm_id and b.b_bk_bll_typ in (BALL_TYPE) AND  ms.n_mtchsts_id in (MATCH_STATUS) and ms.n_mtchsts_id = b.n_bk_sts and
    n_usr_id in (select n_usrmta_id from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    print(match_status)
    print(booking_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type).replace('MATCH_STATUS',match_status))
    booking_data = db_obj.fetch(booking_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type).replace('MATCH_STATUS',match_status))
    print(booking_data)
    print(len(booking_data))
    second_set_json = ''
    for i in range(0, len(booking_data)):
        second_set = second_str.replace('COUNT', str(i)).replace('BOOKING_ID',
                                                                 str(booking_data[i]['bookingid'])).replace(
            'BOOKING_DATE', str(booking_data[i]['bookingdt']))
        second_set = second_set.replace('BOOKING_USER_EMAIL', booking_data[i]['c_usr_eml']).replace(
            'BOOKING_USER_CONTACT', str(booking_data[i]['c_usr_ph']))
        second_set = second_set.replace('BOOKING_HRS', str(booking_data[i]['bookinghrs'])).replace('BOOKING_START_TM',
                                                                                                   str(booking_data[i][
                                                                                                           't_bk_strt']))
        second_set = second_set.replace('BOOKING_END_TIME', str(booking_data[i]['t_bk_end'])).replace('BOOKING_VENUE',
                                                                                                      booking_data[i][
                                                                                                          'c_vn_nm']).replace(
            'BOOKING_VENUE_ID', str(booking_data[i]['venue_id']))
        second_set = second_set.replace('SUPERVISOR_NAME', booking_data[i]['Supervisor_name']).replace('BALL_TYPE',
                                                                                                       booking_data[i][
                                                                                                           'ball_type']).replace(
            'BELOW_AGE_FLAG', str(booking_data[i]['b_bk_blw_age']))
        second_set = second_set.replace('MATCH_STATUS',booking_data[i]['Match_Status'])
        second_set_json += second_set

    final_json = first_str + second_set_json[:-1] + '''}
     }
    }'''

    final_json = eval(final_json)
    print(dict(final_json))
    return final_json

def Customer_Booking_list(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        token = body["token"]
        filter_flag = body["filter"]
        range_val = body["range"]
        query = '''select count(1) from usrmta u where u.n_usrmta_token = "''' + token + '''";'''
        print(query)
        result = database_connect.RunQuery(query)
        if result[0][0] == 1:
            if filter_flag == 0:
                ball_type = '1,2'
                match_status = '0,1,2,3,4'
                result = Booking_data_check(token,ball_type,range_val,match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
            elif filter_flag == 1:
                ball_type = '1,2'
                match_status = '1'
                result = Booking_data_check(token, ball_type, range_val,match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
                #return HttpResponse(json.dumps(result), content_type='application/json')
            elif filter_flag == 2:
                ball_type = '1,2'
                match_status = '3'
                result = Booking_data_check(token, ball_type, range_val, match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
            elif filter_flag == 3:
                ball_type = '1,2'
                match_status = '4'
                result = Booking_data_check(token, ball_type, range_val, match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result = {
                    "code": 1,
                    "msg": "Logged out successfully"
                }
                # logger.log('Invalid Credentials Provided', phone)
                return HttpResponse(json.dumps(result), content_type='application/json')
        elif result[0][0] == 0:
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {
 "code" : 2,
 "msg": "Please check the selected item, if issue persists contact admin"
}

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')


def Booking_data_Search(token,ball_type,range_val,match_status):
    db_obj = database_connect.DBConnection()

    first_str = '''{
     "code" : 1,
     "data": {
      "filter":{
       "min" : 1,
       "max" : RANGE_VAL
      },
      "search":{
       "url": "/sc/searchBooking",
       "min": "3"
      },
      "booking":{'''

    first_str = first_str.replace('RANGE_VAL', str(range_val))

    second_str = '''"COUNT" : {
        "type":"MATCH_STATUS",
        "action_button":[{
         "type":"email",
         "action":"/sc/bookingmanage/match/BOOKING_ID"
        },{
         "type":"edit",
         "action":"/sc/bookingmanage/edit/BOOKING_ID"
        },{
         "type":"cancel",
         "action":"/sc/bookingmanage/can/BOOKING_ID"
        },{
         "type":"download",
         "action" : "/sc/booking/dwnld/BOOKING_ID"
        }],
        "top":{
         "bookingid":"BOOKING_ID",
         "bookingdate":"BOOKING_DATE",
         "bookingmail":"BOOKING_USER_EMAIL",
         "tranid":"TRANSACTION_ID",
         "billingdata":"BILLING_DATE",
         "contact":"BOOKING_USER_CONTACT",
         "bookinghrs":"BOOKING_HRS",
         "time":{
          "start":"BOOKING_START_TM",
          "end":"BOOKING_END_TIME"
         }
        },
        "mid":{
         "venue" : {
          "title" : "BOOKING_VENUE",
           "link" : "/venue/id/BOOKING_VENUE_ID"
         }
        },
        "bottom":{
         "facilities":[{
          "title" : "supervisor",
          "value" : "SUPERVISOR_NAME",
         },{
          "title" : "Ball Type",
          "value" : "BALL_TYPE"
         },{
          "title" : "Kit",
          "value" : "Standard"
         },{
          "title" : "Below 18",
          "Value" : "BELOW_AGE_FLAG"
         },{
          "title" : "Physically Disabled",
          "Value" : "PHY_DISABLE_FLAG"
         }]
        }
       },'''

    booking_query = '''select b.n_bk_id as 'bookingid',b.dt_bk_tmstmp as 'bookingdt',u.c_usr_eml ,u.c_usr_ph ,TIMEDIFF (b.t_bk_end,b.t_bk_strt) as 'bookinghrs',
    b.t_bk_strt ,b.t_bk_end , v.c_vn_nm ,v.n_vn_id as 'venue_id',(select CONCAT(u4.c_usrinfo_frst_nm,' ',u4.c_usrinfo_lst_nm) from users u3,userinfo u4  where u3.n_usr_id=b.n_bk_sup_id and u4.n_usrinfo_usr_id = u3.n_usr_id) as 'Supervisor_name',
    (select bt.c_bltyp_nm  from ball_type bt where bt.n_blyp_id = b.b_bk_bll_typ) as 'ball_type',b.b_bk_blw_age,
    (select ms2.c_mtchsts_nm  from match_status ms2 where ms2.n_mtchsts_id = b.n_bk_sts) as 'Match_Status'
    from booking b , booking_master bm , users u ,usrmta u2 ,venue v ,match_status ms WHERE
    u2.n_usrmta_id = u.n_usr_id AND
    u.n_usr_id = bm.n_bkm_usr AND
    b.n_bk_vn = v.n_vn_id AND
    bm.n_bkm_id = b.n_bk_bkm_id and b.b_bk_bll_typ in (BALL_TYPE) AND  ms.n_mtchsts_id in (MATCH_STATUS) and ms.n_mtchsts_id = b.n_bk_sts and
    n_usr_id in (select n_usrmta_id from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    print(match_status)
    print(booking_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type).replace('MATCH_STATUS',match_status))
    booking_data = db_obj.fetch(booking_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type).replace('MATCH_STATUS',match_status))
    print(booking_data)
    print(len(booking_data))
    second_set_json = ''
    for i in range(0, len(booking_data)):
        second_set = second_str.replace('COUNT', str(i)).replace('BOOKING_ID',
                                                                 str(booking_data[i]['bookingid'])).replace(
            'BOOKING_DATE', str(booking_data[i]['bookingdt']))
        second_set = second_set.replace('BOOKING_USER_EMAIL', booking_data[i]['c_usr_eml']).replace(
            'BOOKING_USER_CONTACT', str(booking_data[i]['c_usr_ph']))
        second_set = second_set.replace('BOOKING_HRS', str(booking_data[i]['bookinghrs'])).replace('BOOKING_START_TM',
                                                                                                   str(booking_data[i][
                                                                                                           't_bk_strt']))
        second_set = second_set.replace('BOOKING_END_TIME', str(booking_data[i]['t_bk_end'])).replace('BOOKING_VENUE',
                                                                                                      booking_data[i][
                                                                                                          'c_vn_nm']).replace(
            'BOOKING_VENUE_ID', str(booking_data[i]['venue_id']))
        second_set = second_set.replace('SUPERVISOR_NAME', booking_data[i]['Supervisor_name']).replace('BALL_TYPE',
                                                                                                       booking_data[i][
                                                                                                           'ball_type']).replace(
            'BELOW_AGE_FLAG', str(booking_data[i]['b_bk_blw_age']))
        second_set = second_set.replace('MATCH_STATUS',booking_data[i]['Match_Status'])
        second_set_json += second_set

    final_json = first_str + second_set_json[:-1] + '''}
     }
    }'''

    final_json = eval(final_json)
    print(dict(final_json))
    return final_json


def Booking_Search(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        token = body["token"]
        filter_flag = body["filter"]
        range_val = body["range"]
        query = '''select count(1) from usrmta u where u.n_usrmta_token = "''' + token + '''";'''
        print(query)
        result = database_connect.RunQuery(query)
        if result[0][0] == 1:
            if filter_flag == 0:
                ball_type = '1,2'
                match_status = '0,1,2,3,4'
                result = Booking_data_Search(token, ball_type, range_val, match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
            elif filter_flag == 1:
                ball_type = '1,2'
                match_status = '1'
                result = Booking_data_Search(token, ball_type, range_val, match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
                # return HttpResponse(json.dumps(result), content_type='application/json')
            elif filter_flag == 2:
                ball_type = '1,2'
                match_status = '3'
                result = Booking_data_Search(token, ball_type, range_val, match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
            elif filter_flag == 3:
                ball_type = '1,2'
                match_status = '4'
                result = Booking_data_Search(token, ball_type, range_val, match_status)
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result = {
                    "code": 1,
                    "msg": "Logged out successfully"
                }
                # logger.log('Invalid Credentials Provided', phone)
                return HttpResponse(json.dumps(result), content_type='application/json')
        elif result[0][0] == 0:
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {
                "code": 2,
                "msg": "Please check the selected item, if issue persists contact admin"
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        return HttpResponse(json.dumps(body), content_type='application/json')
def leader_function(token,ball_type):
    db_obj = database_connect.DBConnection()

    first_json = '''{
     "code" : "1",
     "data":{
      "statistics":{
       "matches" : "LOOP_VAL",
       "runs"  : "MATCH_RUNS",
       "wickets" : "MATCH_WICKETS",
       "catches" : "MATCH_CATCHES",
       "stumpings" : "MATCH_STUMPS",
       "strike rate":"MATCH_SR",
       "Economy" : "MATCH_ECO",
       "highest" : "MATCH_SCORE"
         },
      "board":{
       "top":[{
        "rank" : "1",
        "name" : "HIGH_SCORE_PLAYER",
        "subtitle" : "Highest Score",
        "value" : "HIGH_RUNS"
       },{
        "rank" : "2",
        "name" : "WINNING_TEAMS",
        "subtitle" : "Most winning Team",
        "matches" : "WINS",
        "value" : "WINS"
       },{
        "rank" : "3",
        "name" : "MOM_PLAYER",
        "subtitle" : "Most Man of the Match",
        "value" : "MOM_VALUE"
       },{
        "rank" : "4",
        "name" : "HIGH_WKTS_PLAYER",
        "subtitle" : "Highest wickets in Innings",
        "value" : "WKTS_VALUE"
       },{
        "rank" : "5",
        "name" : "HIGH_FOUR_PLAYER",
        "subtitle" : "Highest boundaries in Innings",
        "value" : "FOURS_VALUE"
       }]
      }
     }
    }'''
    first4_query = '''SELECT bt.c_bltyp_nm ,m.n_mtch_id, m.dt_mtch_strt,v.c_vn_nm  from `match` m ,ball_type bt  ,venue v,innings i  ,ball_summary bs ,overs o where
        bt.n_blyp_id  in (BALL_TYPE) and
        bs.n_bls_ovrs_id = o.n_ovrs_id AND
        o.n_ovrs_inn_id = i.n_inn_id AND
        i.n_inn_mtch_id = m.n_mtch_id AND
        m.n_mtch_vn_id = v.n_vn_id AND
        ( bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
        or  bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'))
        GROUP by bt.c_bltyp_nm ,m.n_mtch_id order by m.n_mtch_id ;'''
    first4_data = db_obj.fetch(first4_query.replace('BALL_TYPE', ball_type).replace('TOKEN_KEY', token))
    # print(first4_data)

    second_set_query = '''select bs.bs_mtch_id,sum(n_bls_run),(sum(bs.n_bls_run)/COUNT(bs.n_bls_id))*100 as 'strike rate',max(n_bls_run),t.c_tm_nm  from ball_summary bs ,team_members tm ,teams t where 
        bs.bs_bll_typ in (BALL_TYPE) and
        bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
        and tm.n_tmb_usr_id = bs.n_bls_btsm_id
        and t.n_tm_id = tm.n_tmb_tm_id
        GROUP by bs.bs_mtch_id,t.c_tm_nm order by bs.bs_mtch_id;'''
    second_set_data = db_obj.fetch(second_set_query.replace('BALL_TYPE', ball_type).replace('TOKEN_KEY', token))
    # print(second_set_data)

    third_query = '''select bs_mtch_id,mr.c_mrs_res ,t.c_tm_nm  from match_result mr ,ball_summary bs,teams t
        where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
        and mr.n_mrs_mtch_id = bs.bs_mtch_id and mr.n_mrs_wn_tm_id = t.n_tm_id group by bs_mtch_id,mr.c_mrs_res ,t.c_tm_nm ;'''
    third_data = db_obj.fetch(third_query.replace('BALL_TYPE', ball_type).replace('TOKEN_KEY', token))
    # print(third_data)

    fourth_set = '''select n_mtch_id ,(select t.c_tm_nm  from teams t where t.n_tm_id = m.n_mtch_tma_id) as 'team name A' ,
        (select t.c_tm_nm  from teams t where t.n_tm_id = m.n_mtch_tmb_id) as 'team name B'
        from `match` m , ball_summary bs  where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'ALAJCOAMKDSLC')
        and bs.bs_mtch_id = m.n_mtch_id GROUP by n_mtch_id ,n_mtch_tma_id ,n_mtch_tmb_id order by m.n_mtch_id;'''
    fourth_data = db_obj.fetch(fourth_set.replace('BALL_TYPE', ball_type).replace('TOKEN_KEY', token))
    # print(fourth_data)

    fifth_query = '''select bs.bs_mtch_id,sum(n_bls_run),tm.n_tmb_usr_id,(select count(1) as 'wkts'  from ball_summary bss where bss.n_bls_bwlr_id = tm.n_tmb_usr_id and n_bls_wkt_typ in (1,2,4,7)) as 'wkts' ,
        (select count(1) as 'catches' from ball_summary bs where bs.n_bls_wkt_ass_id  = tm.n_tmb_usr_id and  n_bls_wkt_typ = 4) as 'catches' ,
        (select count(1) as 'stumpings' from ball_summary bs where bs.n_bls_wkt_ass_id = tm.n_tmb_usr_id and  n_bls_wkt_typ = 3) as 'stumpings' ,
        (sum(bs.n_bls_run)/(COUNT(bs.n_bls_id)/6)) as 'Economy',t.c_tm_nm  from ball_summary bs ,team_members tm ,teams t where bs.bs_bll_typ in (BALL_TYPE) and bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
        and tm.n_tmb_usr_id = bs.n_bls_bwlr_id
        and t.n_tm_id = tm.n_tmb_tm_id
        GROUP by bs.bs_mtch_id,t.c_tm_nm,tm.n_tmb_usr_id  ;'''
    fifth_data = db_obj.fetch(fifth_query.replace('BALL_TYPE', ball_type).replace('TOKEN_KEY', token))
    matches_query = '''select count(DISTINCT n_inn_mtch_id) as 'matches' from innings i where n_inn_id in
    (select n_ovrs_inn_id  from overs o where n_ovrs_id in
    (select n_bls_ovrs_id  from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and ( bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    or  bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'))));'''
    matches_total = db_obj.fetch(matches_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0][
        'matches']
    # print(matches_total)
    # Total_runs
    runs_query = '''select sum(n_bls_run) as 'runs' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and (   bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'));'''
    total_runs = db_obj.fetch(runs_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0]['runs']
    # print(total_runs)
    # total wkts
    wkts_query = '''select count(1) as 'wkts' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and  bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and n_bls_wkt_typ in (1,2,4,7);'''
    total_wkts = db_obj.fetch(wkts_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0]['wkts']
    # print(total_wkts)
    # total catches
    catches_query = '''select count(1) as 'catches' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and  bs.n_bls_wkt_ass_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and n_bls_wkt_typ = 4;'''
    total_Catches = db_obj.fetch(catches_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0][
        'catches']
    # print(total_Catches)
    # Total Stumpings
    stumpings_total = '''select count(1) as 'stumpings' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and  bs.n_bls_wkt_ass_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY')
    and n_bls_wkt_typ  = 3;'''
    total_stumps = db_obj.fetch(stumpings_total.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0][
        'stumpings']
    # print(total_stumps)
    strike_rate_query = '''select (sum(bs.n_bls_run)/COUNT(bs.n_bls_id))*100 as 'strike rate'  from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and  bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    sr_total = db_obj.fetch(strike_rate_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0][
        'strike rate']
    # print(sr_total)
    eco_query = '''select (sum(bs.n_bls_run)/(COUNT(bs.n_bls_id)/6)) as 'Economy'  from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and  bs.n_bls_bwlr_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY');'''
    eco_total = db_obj.fetch(eco_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0]['Economy']
    # print(eco_total)
    highest_runs_query = '''select max(n_bls_run) as 'highest_runs' from ball_summary bs where bs.bs_bll_typ in (BALL_TYPE) and (   bs.n_bls_btsm_id  in (select n_usrmta_usr_id  from usrmta u where n_usrmta_token = 'TOKEN_KEY'));'''
    high_runs = db_obj.fetch(highest_runs_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))[0][
        'highest_runs']
    i = 0
    replace_str = first_json.replace('LOOP_VAL', str(i)).replace('BALL_TYPE', first4_data[i]['c_bltyp_nm']).replace(
        'TEAMA', fourth_data[i]['team name A']).replace('TEAMB', fourth_data[i]['team name B']).replace(
        'MATCH_DATE', str(first4_data[i]['dt_mtch_strt'])).replace('VENUE_NAME', first4_data[i]['c_vn_nm']).replace(
        'PLAYERS_TEAM', second_set_data[i]['c_tm_nm']).replace('MATCH_RUNS',
                                                               str(second_set_data[i]['sum(n_bls_run)']))
    replace_str = replace_str.replace('MATCH_WICKETS', str(fifth_data[i]['wkts'])).replace('MATCH_CATCHES', str(
        fifth_data[0]['catches'])).replace('MATCH_STUMPS', str(fifth_data[i]['stumpings'])).replace('MATCH_SR', str(
        second_set_data[i]['strike rate']))
    replace_str = replace_str.replace('MATCH_ECO', str(fifth_data[i]['Economy'])).replace('MATCH_SCORE', str(
        fifth_data[i]['sum(n_bls_run)'])).replace('WINNING_TEAM', third_data[i]['c_tm_nm']).replace('WINNING_STATS',
                                                                                                    third_data[i][
                                                                                                        'c_mrs_res'])

    first_json1 = replace_str.replace('PLAYER_MATCHES', str(matches_total)).replace('PLAYER_RUNS', str(total_runs))
    first_json1 = first_json1.replace('PLAYER_WICKETS', str(total_wkts)).replace('PLAYER_CTACHES',
                                                                                 str(total_Catches)).replace(
        'PLAYER_STUMPINGS', str(total_stumps)).replace('PLAYER_SR', str(sr_total)).replace('PLAYER_ECO',
                                                                                           str(eco_total)).replace(
        'PLAYER_HR', str(high_runs))

    high_runs_query = '''select bs_mtch_id,n_bls_btsm_id ,CONCAT(u.c_usrinfo_frst_nm,' ',u.c_usrinfo_lst_nm) as 'High_Score_Player',
    (select sum(n_bls_run) from ball_summary bs1 where bs1.bs_mtch_id=bs.bs_mtch_id and bs1.n_bls_btsm_id=bs.n_bls_btsm_id )  as 'Highest_Score'
    from ball_summary bs,userinfo u where bs.bs_bll_typ in (BALL_TYPE) and  u.n_usrinfo_id = bs.n_bls_btsm_id  group by bs_mtch_id ,n_bls_btsm_id order by Highest_Score DESC ;'''
    highest_scores = db_obj.fetch(high_runs_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))

    winning_query = '''select n_mrs_wn_tm_id,t.c_tm_nm ,count(n_mrs_wn_tm_id) as 'wins' from match_result mr,teams t where
    n_mrs_wn_tm_id = t.n_tm_id
    group by n_mrs_wn_tm_id order by wins DESC ;'''
    win_max = db_obj.fetch(winning_query.replace('TOKEN_KEY', token))

    mom_query = '''select n_mrs_mom_id,(select CONCAT(u.c_usrinfo_frst_nm,' ',u.c_usrinfo_lst_nm) as 'Full_Name' from userinfo u where u.n_usrinfo_usr_id =mr.n_mrs_mom_id  )as 'MOM_Player',
    count(n_mrs_mom_id) from match_result mr group by n_mrs_mom_id order by n_mrs_mom_id desc;'''
    mom_max = db_obj.fetch(mom_query.replace('TOKEN_KEY', token))

    high_wkt_query = '''select bs.n_bls_bwlr_id ,o.n_ovrs_inn_id,(select CONCAT(u.c_usrinfo_frst_nm,' ',u.c_usrinfo_lst_nm) as 'Full_Name' from userinfo u where u.n_usrinfo_usr_id =bs.n_bls_bwlr_id  )as 'Best_Wkts',
    count(bs.b_bls_wkt) as 'Total_Wkts' from ball_summary bs ,overs o WHERE
    bs.bs_bll_typ in (BALL_TYPE) and
    bs.n_bls_ovrs_id = o.n_ovrs_id
    and bs.b_bls_wkt  = 1  group by bs.n_bls_bwlr_id,o.n_ovrs_inn_id order by Total_Wkts desc  ;'''
    wkt_max = db_obj.fetch(high_wkt_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))

    high_fours_query = '''select bs.n_bls_ns_btsm_id  ,o.n_ovrs_inn_id,(select CONCAT(u.c_usrinfo_frst_nm,' ',u.c_usrinfo_lst_nm) as 'Full_Name' from userinfo u where u.n_usrinfo_usr_id =bs.n_bls_ns_btsm_id  )as 'Best_Fours',
    count(bs.b_bls_wkt) as 'Total_Boundries' from ball_summary bs ,overs o WHERE
    bs.bs_bll_typ in (BALL_TYPE) and
    bs.n_bls_ovrs_id = o.n_ovrs_id
    and bs.n_bls_run in (4,6) and bs.b_bls_xtr = 0 group by bs.n_bls_ns_btsm_id,o.n_ovrs_inn_id order by Total_Boundries desc  ;'''
    fours_max = db_obj.fetch(high_fours_query.replace('TOKEN_KEY', token).replace('BALL_TYPE', ball_type))

    first_json1 = first_json1.replace('PLAYER_MATCHES', str(matches_total)).replace('PLAYER_RUNS', str(total_runs))
    first_json1 = first_json1.replace('PLAYER_WICKETS', str(total_wkts)).replace('PLAYER_CTACHES',
                                                                                 str(total_Catches)).replace(
        'PLAYER_STUMPINGS', str(total_stumps)).replace('PLAYER_SR', str(sr_total)).replace('PLAYER_ECO',
                                                                                           str(eco_total)).replace(
        'PLAYER_HR', str(high_runs))
    first_json1 = first_json1.replace('HIGH_SCORE_PLAYER', highest_scores[0]['High_Score_Player']).replace('HIGH_RUNS',
                                                                                                           str(highest_scores[
                                                                                                               0][
                                                                                                               'Highest_Score']))
    first_json1 = first_json1.replace('WINNING_TEAMS', win_max[0]['c_tm_nm']).replace('WINS',
                                                                                             str(win_max[0]['wins']))
    first_json1 = first_json1.replace('MOM_PLAYER', mom_max[0]['MOM_Player']).replace('MOM_VALUE',
                                                                                             str(mom_max[0][
                                                                                                 'count(n_mrs_mom_id)']))
    first_json1 = first_json1.replace('HIGH_WKTS_PLAYER', str(wkt_max[0]['Best_Wkts'])).replace('WKTS_VALUE',
                                                                                                  str(wkt_max[0][
                                                                                                      'Total_Wkts']))
    first_json1 = first_json1.replace('HIGH_FOUR_PLAYER', str(fours_max[0]['Best_Fours'])).replace('FOURS_VALUE',
                                                                                                   str(fours_max[0][
                                                                                                       'Total_Boundries']))

    final_json2 = eval(first_json1)
    return final_json2


def Leader_Stats(request):
    if request.method == "GET":#Expecting the function to give proper response for GET
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        token = body["token"]
        filter = body["filter"]
        sub_filter = body["sub_filter"]

        query = '''select count(1) from usrmta u where u.n_usrmta_token = "'''+token+'''";'''
        result = database_connect.RunQuery(query)
        if result[0][0]==1:#if the token is right then this checks in
            if filter == 3 and sub_filter == 0:
                ball_type = '1,2'
                final_json = leader_function(token,ball_type)
                return HttpResponse(json.dumps(final_json), content_type='application/json')
            elif filter == 3 and sub_filter == 1:
                ball_type = '1'
                final_json = leader_function(token, ball_type)
                return HttpResponse(json.dumps(final_json), content_type='application/json')
            elif filter == 3 and sub_filter == 2:
                ball_type = '2'
                final_json = leader_function(token, ball_type)
                return HttpResponse(json.dumps(final_json), content_type='application/json')
            else:  # Any other value is handled here
                result = {
                    "code": 1,
                    "msg": "User Input error"
                }

                return HttpResponse(json.dumps(result), content_type='application/json')
        elif result[0][0] == 0:#if token is not proper then Logout fails
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:#Any other value is handled here
            result = {
                "code": 1,
                "msg": "Logout Failed"
            }

            return HttpResponse(json.dumps(result), content_type='application/json')
    elif request.method == "POST":#For the POST request it just prints the input request itself.
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        return HttpResponse(json.dumps(body), content_type='application/json')