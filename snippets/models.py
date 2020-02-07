import threading

from django.db import models
# Create your models here.
from .settings import *
import mysql.connector
import openpyxl
import pandas as pd


def ImportFromXLSX(excel_file):
    # wb = openpyxl.load_workbook(excel_file, read_only=True)
    xl = pd.ExcelFile(excel_file)
    print(xl.sheet_names)
    cnx = None
    try:
        cnx = mysql.connector.connect(host=DB_CONFIG["HOST"], user=DB_CONFIG["USER"],
                                      password=DB_CONFIG["PASSWORD"], database=DB_CONFIG["DATABASE"])
    except mysql.connector.Error as err:
        print('mysql connect err=={}', err)

    params =["code", "serial_num", "value"]

    duplicates = []
    params_str = ",".join(params)
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name, header=None)
        for val in df.values:
            cursor = cnx.cursor()
            insert_sql = "INSERT INTO {}({}) SELECT '{}', '{}', '{}' WHERE NOT EXISTS(SELECT 1 FROM {} " \
                         "WHERE {}='{}')".format(DB_CONFIG["TABLE"], params_str, val[0], val[1], val[2],
                                                 DB_CONFIG["TABLE"], "code", val[0])
            cursor.execute(insert_sql)
            if cursor.rowcount == 0:
                duplicates.append((val[0], val[1]))
            else:
                cnx.commit()
            cursor.close()
    return duplicates


class Snippet(models.Model):
    serial_num = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    date_time = models.DateTimeField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Snippet'
        verbose_name_plural = "Snippet"

