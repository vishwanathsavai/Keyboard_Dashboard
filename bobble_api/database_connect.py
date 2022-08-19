'''
*	File Name	view.py
*	Created By	Vishwanath P
*	Reviewed By
*	Description	About the files
    DB connection script which will be used to connect to DB. It comprises of class which is used for DB connections, running queries and ending of connection.
*	Version	1
*	Sl No	Author	        Reviewer	Date	    Version	 Changes
*	1	    Vishwanath P	Rajeeva B	01/Jul/22	0.1	     Initial Draft
'''
import pymysql

#Database connection class
class DBConnection:
    def __init__(self):
        self.host = "167.71.230.0"
        self.port = 3366
        self.user = "root"
        self.password = "Nofy@9663691607@DataBase"
        self.db = "bobble"
        print("Initialised")

    def __connect__(self):
        self.con = pymysql.connect(host=self.host,db=self.db,port=self.port, user=self.user, password=self.password,autocommit=True)# cursorclass=pymysql.cursors.DictCursor,
        self.cur = self.con.cursor()
        print("Connection done")

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        print(result)
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()

import psycopg2

#Database connection class for Redshift
class RS_DBConnection:
    def __init__(self):
        self.host = "redshift-cluster-bobble-mid.cbkrwni00iub.ap-south-1.redshift.amazonaws.com"
        self.port = 5439
        self.user = "rajeev"
        self.password = "Rajeev@qwfytr#%6"
        self.db = "prod"
        print("Initialised")

    def __connect__(self):
        self.con = psycopg2.connect(host=self.host,dbname=self.db,port=self.port, user=self.user, password=self.password)# cursorclass=pymysql.cursors.DictCursor,
        self.cur = self.con.cursor()
        print("Connection done")

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        print(result)
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()


def RunQuery(query):
    conn = pymysql.connect(host='167.71.230.0', port=3366, user='root', passwd='Nofy@9663691607@Database', db='bobble',autocommit=True)
    cur = conn.cursor()

    cur.execute(query)

    result = cur.fetchall()
    conn.close()
    print(result)
    #conn.autocommit(True)
    return (result)