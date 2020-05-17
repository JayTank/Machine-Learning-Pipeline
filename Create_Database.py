import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql


dbname = "postgres"
nisdb = "nis_database"
user = "postgres"
host = "localhost"
password = "Qwerty@94"

def connectdb(dbname, user, host, password):
    con = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier("nis_database"))
        )
    except:
        pass
    finally:
        # closing database connection.
        if (con):
            cur.close()
            con.close()


def connectnisdb(nisdb, user, host, password):
    con = psycopg2.connect(dbname=nisdb, user=user, host=host, password=password)
    con.autocommit = True
    return con

connectdb(dbname, user, host, password)
con = connectnisdb(nisdb, user, host, password)
cur = con.cursor()
