from django.db import models
import cx_Oracle
from django.db import connection


def get_subscription_types():
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_SUBSCRIPTION_TYPES", (2, ref_cursor))
    raw_context = result[1].fetchall()
    subscription_ids = []
    subscription_types = []
    subscription_descs = []
    subscription_prices = []
    for i in range(len(raw_context)):
        subscription_ids.append(raw_context[i][0])
        subscription_types.append(raw_context[i][1])
        subscription_descs.append(raw_context[i][2])
        subscription_prices.append(raw_context[i][3])
    return subscription_ids, subscription_types, subscription_descs, subscription_prices


def get_players():
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_PLAYERS", (2, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context

def get_matches(user_id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_MATCHES", (user_id, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context

def get_current_user_email(user_id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_USER_EMAIL", (user_id, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context

def get_predictions(user_id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_PREDICTIONS", (user_id, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context




class TSubscriptionType(models.Model):
    type_id = models.FloatField(primary_key=True)
    type_name = models.CharField(max_length=500, blank=True, null=True)
    type_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_subscription_type'



def get_subscription_types_by_id(id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_SUBSCRIPTION_TYPES_BY_ID", (id, ref_cursor))
    raw_context = result[1].fetchall()
    subscription_ids = []
    subscription_types = []
    subscription_prices = []
    for i in range(len(raw_context)):
        subscription_ids.append(raw_context[i][0])
        subscription_types.append(raw_context[i][1])
        subscription_prices.append(raw_context[i][2])
    return subscription_ids, subscription_types, subscription_prices


def insert_new_user_sub(id, user_id):
    print(user_id)
    cursor = connection.cursor()
    days = 0
    if id == 1:
        days = 7
    else:
        days = 30
    result  = cursor.callproc("SP_LOAD_NEW_SUBSCRIPTION", (user_id, id, days))
    return 'success'


def get_matches_by_name(name):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_MATCHES_BY_NAME", (name, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context


def insert_new_user_prediction(name, user_id):
    cursor = connection.cursor()
    result  = cursor.callproc("SP_LOAD_NEW_USER_PREDICTION", (name, user_id))
    return 'success'


def get_subs_analysis():
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_SUBSCRIPTION_ANALYSIS", (2, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context


def get_current_user_predictions_amount(user_id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_CURRENT_USER_PREDICTIONS_AMOUNT", (user_id, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context


def get_current_user_subscription(user_id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_CURRENT_USER_SUBSCRIPTION", (user_id, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context


def get_matches_by_player_id(player_id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_MATCHES_BY_PLAYER_ID", (player_id, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context


def get_players_by_id(player_id):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_PLAYERS_BY_ID", (player_id, ref_cursor))
    raw_context = result[1].fetchall()
    return raw_context


def get_subs_analysis_by_date(date_from, date_to):
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_SUBSCRIPTION_ANALYSIS_BY_DATE", (date_from, date_to, ref_cursor))
    raw_context = result[2].fetchall()
    return raw_context


def load_new_today_matches():
    cursor = connection.cursor()
    ref_cursor  = cursor.var(cx_Oracle.CURSOR).var
    result  = cursor.callproc("SP_GET_NEW_DATE_FLAG", (1, ref_cursor))
    raw_context = result[1].fetchall()  
    print(raw_context)  
    flag_new_date = raw_context[0][0]
    print('FLAG_NEW_DATE==', flag_new_date)
    if flag_new_date > 1:
        import http.client
        import json
        import pandas as pd
        from cx_Oracle import DatabaseError
        from datetime import datetime
        

        print(datetime.today().strftime('%Y-%m-%d'))
        
        conn = http.client.HTTPSConnection("tennis-live-data.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': "57fcc65541msh4841dc21fef332dp1f0486jsn7e8c59408325",
            'X-RapidAPI-Host': "tennis-live-data.p.rapidapi.com"
            }

        print(datetime.today().strftime('%Y-%m-%d'))
        req_str = "/matches-by-date/" + datetime.today().strftime('%Y-%m-%d')

        conn.request("GET", req_str , headers=headers)

        res = conn.getresponse()
        data_match_example = res.read()
        dictDataMatch = json.loads(data_match_example.decode("utf-8"))
        DataMatchList = []
        for j in range(0, len(dictDataMatch['results'])):
            for i in dictDataMatch['results'][j]['matches']:
                DataMatchList.append((i['id'], i['title'], i['home_id'], i['away_id'], i['date'], dictDataMatch['results'][j]['tournament']['name']+ ' , ' +i['round_name']))
        
        column_names=["id","match_name","first_player_id", "second_player_id", "match_date", "match_desc"]
        df=pd.DataFrame(DataMatchList,columns=column_names)
        try:
            conn = cx_Oracle.connect(user="system", password="ADMIN",
                                    dsn="192.168.56.1:1521/xe",
                                    encoding="UTF-8")
            if conn:
                print("cx_Oracle version:", cx_Oracle.version)
                print("Database version:", conn.version)
                print("Client version:", cx_Oracle.clientversion())
                
                # Now execute the sqlquery 
                cursor = conn.cursor()
                print("You're connected.................")
                
                # Drop table if exists
                print('Droping raw_players_from_live_api table if exists............')
                cursor.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE raw_matches_from_live_api'; EXCEPTION WHEN OTHERS THEN NULL; END;")
                
                print('Creating table raw_players_from_live_api............')
                cursor.execute("CREATE TABLE raw_matches_from_live_api (id number, match_name varchar(500), first_player_id number, second_player_id number, match_date varchar(500),match_desc varchar(500))")
                print("raw_players_from_live_api table is created..............")
        except DatabaseError as e:
            err, = e.args
            print("Oracle-Error-Code:", err.code)
            print("Oracle-Error-Message:", err.message)
        finally:
            cursor.close()
            conn.close()
        try:
            conn = cx_Oracle.connect(user="system", password="ADMIN",
                                    dsn="192.168.56.1:1521/xe",
                                    encoding="UTF-8")
            if conn:
                print("cx_Oracle version:", cx_Oracle.version)
                print("Database version:", conn.version)
                print("Client version:", cx_Oracle.clientversion())
                cursor = conn.cursor()
                print("You're connected: ")
                print('Inserting data into table....')
                for i,row in df.iterrows():
                    sql = "INSERT INTO raw_matches_from_live_api(id,match_name,first_player_id,second_player_id,match_date, match_desc) VALUES(:1,:2,:3,:4,:5, :6)"
                    cursor.execute(sql, tuple(row))
                # the connection is not autocommitted by default, so we must commit to save our changes
                conn.commit()
                print("Record inserted succesfully")
        except DatabaseError as e:
            err, = e.args
            print("Oracle-Error-Code:", err.code)
            print("Oracle-Error-Message:", err.message)
        finally:
            cursor.close()
            conn.close()
        
        cursor = connection.cursor()
        result  = cursor.callproc("SP_UPDATE_MAX_DATE", (1, 1))