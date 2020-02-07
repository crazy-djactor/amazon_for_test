from celery import Celery
import mysql.connector
import pandas as pd
from celery import shared_task
from snippets.models import SnippetHistory
from testproject.settings import DB_CONFIG
from datetime import datetime

app = Celery('tasks', broker='redis://localhost')

@app.task
def add(x, y):
    return x + y

@shared_task
def ImportFromXLSX(excel_file):
    xl = pd.ExcelFile(excel_file)
    print(xl.sheet_names)
    cnx = None
    try:
        cnx = mysql.connector.connect(host=DB_CONFIG["HOST"], user=DB_CONFIG["USER"],
                                      password=DB_CONFIG["PASSWORD"], database=DB_CONFIG["DATABASE"])
    except mysql.connector.Error as err:
        print('mysql connect err=={}', err)

    params =["code", "serial_num", "value"]

    params_str = ",".join(params)
    duplicates = []
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name, header=None)
        for val in df.values:
            cursor = cnx.cursor()
            insert_sql = "INSERT INTO {}({}) SELECT '{}', '{}', '{}' WHERE NOT EXISTS(SELECT 1 FROM {} " \
                         "WHERE {}='{}')".format(DB_CONFIG["TABLE"], params_str, val[0], val[1], val[2],
                                                 DB_CONFIG["TABLE"], "code", val[0])
            cursor.execute(insert_sql)
            if cursor.rowcount == 0:
                SnippetHistory.objects.create(code=val[0], serial_num=val[1], date_time=datetime.now())
                duplicate = {"code": val[0], "serial_num": val[1], "value" : val[2]}
                duplicates.append(duplicate)
            else:
                cnx.commit()
            cursor.close()
    return duplicates