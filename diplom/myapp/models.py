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