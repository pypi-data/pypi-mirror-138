import math
import urllib.parse
import warnings

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

import pyodbc
import numpy as np
import os

os.environ["MODIN_ENGINE"] = "ray"
import modin.pandas as pd
import cx_Oracle
import pymysql
from sqlalchemy import create_engine, text
import json


def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    return df


def load_config(path_file_config, server, database):
    server = str(server).upper()
    database = str(database).lower()

    with open(path_file_config) as json_file:
        data = json.load(json_file)
    if data.get(server):
        if data.get(server).get(database):
            print(f"Server and Database are Correct: {server}/{database}")
            data = data[server][database]
        else:
            print(f"Server or Database are incorrect: {server}/{database}")
            data = dict()
    else:
        if not data.get(server):
            print(f"file config.json  Server:{server}  not exists")
            data = dict()
    return data


class Core(object):

    @staticmethod
    def to_sql(df, con, table="", schema=None):
        def chunker(seq, size):
            return (seq[pos: pos + size] for pos in range(0, len(seq), size))

        CHUNK_LIMIT = 2099
        chunksize = math.floor(CHUNK_LIMIT / len(df.columns))
        for chunk in chunker(df, chunksize):
            chunk.to_sql(
                name=table,
                con=con,
                if_exists="append",
                index=False,
                schema=schema,
                method="multi",
            )

    @staticmethod
    def database_query(file_config, server=None, database=None, query=None, is_sql_direct=False):
        parameter = load_config(file_config, server, database)

        print("Loading connection...")
        if str(server).lower() == 'sqlserver':
            if not parameter["authentication"]:
                params = 'DRIVER={0};' \
                         'SERVER={1};' \
                         'PORT={2};' \
                         'DATABASE={3};' \
                         'Trusted_Connection=yes'.format(
                    parameter["driver"], parameter["host"], parameter["port"], parameter["db"])
            else:
                params = 'DRIVER={0};' \
                         'SERVER={1};' \
                         'PORT={2};' \
                         'DATABASE={3};' \
                         'UID={4};' \
                         'PWD={5};'.format(
                    parameter["driver"], parameter["host"], parameter["port"], parameter["db"],
                    parameter["username"], parameter["password"])
            params = urllib.parse.quote_plus(params)
            engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params, fast_executemany=True)
            con = engine.connect()

            if is_sql_direct:
                con.execute(query)
                con.close()
                print("Finished query")
                return True
            else:
                df = pd.read_sql(query, con=con)
                df = reduce_mem_usage(df)
                print("Finished query")
                return df, con

        elif str(server).lower() == 'oracle':
            dsn_tns = cx_Oracle.makedsn(parameter["host"], parameter["port"], parameter["db"])
            print(dsn_tns)
            con = cx_Oracle.connect(parameter["username"], parameter["password"], dsn_tns)

            if is_sql_direct:
                con.autocommit = True
                cursor = con.cursor()
                cursor.execute(query)
                con.close()
                print("Finished query")
                return True
            else:
                df = pd.read_sql(query, con=con)
                df = reduce_mem_usage(df)
                print("Finished query")
                return df, con

        elif str(server).lower() == 'mysql':
            if is_sql_direct:
                db = pymysql.connect(host=parameter["host"], port=parameter["port"],
                                     user=parameter["username"], passwd=parameter["password"],
                                     db=parameter["db"], autocommit=True)
                cur = db.cursor(pymysql.cursors.DictCursor)
                cur.execute(query)
                db.close()
                print("Finished query")
                return True
            else:
                engine = create_engine("{0}://{1}:{2}@{3}:{4}/{5}".format(
                    parameter["driver"], parameter["username"], parameter["password"],
                    parameter["host"], parameter["port"], parameter["db"]))
                con = engine.connect()
                df = pd.read_sql(text(query), engine)
                print("Finished query")
                return df, con

        elif str(server).lower() == 'aster':
            con = pyodbc.connect("DRIVER={0};SERVER={1};PORT={2};"
                                 "DATABASE={3};UID={4};PWD={5}".format(
                parameter["driver"], parameter["host"], parameter["port"], parameter["db"],
                parameter["username"], parameter["password"]))

            if is_sql_direct:
                con.autocommit = True
                cursor = con.cursor()
                cursor.execute(query)
                con.close()
                print("Finished query")
                return True
            else:
                df = pd.read_sql(query, con=con)
                df = reduce_mem_usage(df)
                print("Finished query")
                return df, con

        elif str(server).lower() == 'teradata':
            con = pyodbc.connect("DRIVER={0};DBCNAME={1};PORT={2};"
                                 "DATABASE={3};UID={4};PWD={5}".format(
                parameter["driver"], parameter["host"], parameter["port"], parameter["db"],
                parameter["username"], parameter["password"]))

            if is_sql_direct:
                con.autocommit = True
                cursor = con.cursor()
                cursor.execute(query)
                con.close()
                print("Finished query")
                return True
            else:
                df = pd.read_sql(query, con=con)
                df = reduce_mem_usage(df)
                print("Finished query")
                return df, con
