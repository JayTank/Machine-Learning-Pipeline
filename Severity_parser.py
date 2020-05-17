from Create_Database import connectnisdb, connectdb
import psycopg2
import os

dbname = "postgres"
nisdb = "nis_database"
user = "postgres"
host = "localhost"
password = "Qwerty@94"
severity_files = os.listdir("nis_severity_files")
severity_data_files = os.listdir("nis_severity_data_files")

def createseveritytable(cur):
    i = 0
    for file in severity_files:
        file_name = os.path.basename(file).split('_')
        table_name = 'NIS_' + file_name[2] + '_SEVERITY'
        with open(os.path.abspath(os.path.join('nis_severity_files', file)), 'r') as f:
            data = f.readlines()
            data_list = data[12:15] + data[16:17]
            col_data = [item[:6].split("- ") for item in data_list]
            column_name = col_data[0]
            start = col_data[1]
            end = col_data[2]
            col_type = col_data[3]
            sql_data = [[item[int(column_name[0]) - 1: int(column_name[1])].strip(),
                    item[int(start[0]) - 1: int(start[1])].strip(),
                    item[int(end[0]) - 1: int(end[1])].strip(),
                    item[int(col_type[0]) - 1: int(col_type[1])].strip()] for item in data[20:]]
            severity_table_column_name = [item[0] + ' INTEGER NOT NULL' if item[3] == 'Num' else item[0] + ' CHARACTER(30) NOT NULL' for item in sql_data]
        try:
            create_table_query = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (' + ', '.join(severity_table_column_name) + ');'
            cur.execute(create_table_query)
            print("Table created successfully in PostgreSQL", table_name)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)

        while True:
                insert_severity_data(sql_data, severity_data_files[i])
                i += 1
                if i <= len(severity_data_files):
                    break


def insert_severity_data(sql_data, filename):
    table_name = 'NIS_' + filename.split('_')[1] + '_SEVERITY'
    sql_column_name = [item[0] for item in sql_data]
    with open(os.path.abspath(os.path.join('nis_severity_data_files', filename)), 'r') as f:
        all_data = f.readlines()
        for data in all_data:
            record_to_insert = [data[int(item[1])-1:int(item[2])].strip() for item in sql_data]
            postgres_insert_query = 'INSERT INTO ' + table_name + '(' + ', '.join(sql_column_name) + ') VALUES (' + ', '.join(record_to_insert) + ');'
            try:
                cur.execute(postgres_insert_query)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed to insert record into " + table_name, error)

        print("Record inserted successfully into " + table_name)


connectdb(dbname, user, host, password)
con = connectnisdb(nisdb, user, host, password)
cur = con.cursor()
createseveritytable(cur)

