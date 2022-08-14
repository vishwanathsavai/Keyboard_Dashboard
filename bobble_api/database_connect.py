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
        self.host = "134.209.159.4"
        self.port = 3366
        self.user = "root"
        self.password = "MintAdz@1234"
        self.db = "bobble"
        print("Initialised")

    def __connect__(self):
        self.con = pymysql.connect(host=self.host,port=self.port, user=self.user, password=self.password, db=self.db, cursorclass=pymysql.cursors.DictCursor,autocommit=True)
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
    conn = pymysql.connect(host='134.209.159.4', port=3366, user='root', passwd='MintAdz@1234', db='cric',autocommit=True)
    cur = conn.cursor()

    cur.execute(query)

    result = cur.fetchall()
    conn.close()
    print(result)
    #conn.autocommit(True)
    return (result)