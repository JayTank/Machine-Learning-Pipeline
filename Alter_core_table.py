from Create_Database import connectnisdb, connectdb
import psycopg2
import os

dbname = "postgres"
nisdb = "nis_database"
user = "postgres"
host = "localhost"
password = "Qwerty@94"
core_files = os.listdir("nis_core_files")

connectdb(dbname, user, host, password)
con = connectnisdb(nisdb, user, host, password)
cur = con.cursor()

for file in core_files:
    file_name = os.path.basename(file).split('_')
    table_name = 'NIS_' + file_name[2] + '_Core'
    print(table_name)
    try:
        cur.execute("ALTER TABLE IF EXISTS %s ADD id serial" % table_name)
        cur.execute("ALTER TABLE IF EXISTS %s ADD disease_code VARCHAR(30) DEFAULT ''" % table_name)
        cur.execute("ALTER TABLE IF EXISTS %s ADD status INTEGER DEFAULT 0" % table_name)
        print("columns updated successfully in table " + table_name)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

con.commit()
cur.close()
con.close()
