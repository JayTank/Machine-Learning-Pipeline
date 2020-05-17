from Create_Database import connectnisdb, connectdb
import psycopg2
import os

dbname = "postgres"
nisdb = "nis_database"
user = "postgres"
host = "localhost"
password = "Qwerty@94"
dxpr_files = os.listdir("dxpr_grps_files")
dxpr_data_files = os.listdir("dxpr_grps_data_files")

def createdpgtable(cur):
    i = 0
    for file in dxpr_files:
        file_name = os.path.basename(file).split('_')
        table_name = 'NIS_' + file_name[2] + '_DX_PR_GRPS'
        with open(os.path.abspath(os.path.join('dxpr_grps_files', file)), 'r') as f:
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
            core_table_column_name = [item[0] + " INTEGER DEFAULT 0" if item[3] == 'Num' else item[0] + " VARCHAR(30)" for item in sql_data]
            try:
                create_table_query = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (' + ', '.join(core_table_column_name) + ');'
                cur.execute(create_table_query)
                print("Table created successfully in PostgreSQL", table_name)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while creating PostgreSQL table", error)

            while True:
                insert_dpg_data(sql_data, dxpr_data_files[i])
                i += 1
                if i <= len(dxpr_data_files):
                    break


def insert_dpg_data(sql_data, filename):
    table_name = 'NIS_' + filename.split('_')[1] + '_DX_PR_GRPS'
    sql_column_name = [item[0] for item in sql_data]

    with open(os.path.abspath(os.path.join('dxpr_grps_data_files', filename)), 'r') as f:
        all_data = f.readlines()
        for data in all_data:
            record_to_insert = list()
            for item in sql_data:
                data_to_insert = data[int(item[1])-1:int(item[2])].strip()
                if item[3] == 'Char':
                    data_to_insert = "'" + data_to_insert + "'"
                record_to_insert.append(data_to_insert)
            postgres_insert_query = "INSERT INTO " + table_name + "(" + ", ".join(sql_column_name) + ") VALUES (" + ", " .join(record_to_insert) + ");"
            try:
                cur.execute(postgres_insert_query)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed to insert record into " + table_name, error)


connectdb(dbname, user, host, password)
con = connectnisdb(nisdb, user, host, password)
cur = con.cursor()
createdpgtable(cur)
cur.close()
con.close()
