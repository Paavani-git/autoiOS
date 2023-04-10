import sqlite3
from sqlite3 import Error
import os


def create_table(table_name):
    if table_name == "Source_Table":
        cur.execute("""CREATE TABLE IF NOT EXISTS {} (
                library_name text,
                version text
        )""".format(table_name))
    elif table_name == "Child_Table":
        cur.execute("""CREATE TABLE IF NOT EXISTS {} (
                function_name text,
                Hash text,
                source_id integer
        )""".format(table_name))

    print("-> List of Tables")
    cur.execute('SELECT name from sqlite_master where type="table"')
    print(cur.fetchall())

def print_table(table_name):
    print("-> Tablename = " + table_name)
    query = "SELECT rowid, * FROM %s;" % table_name
    for row in cur.execute(query):
        print(row)

def transfer():
    sigs_path = str(input("Enter the sig files path (include '/' at the end): "))
    os.chdir(sigs_path)
    files_list = os.listdir(sigs_path)
    #print(files_list)
    #print(len(files_list))

    for every_file in files_list:
        library_name, version, tmp = every_file.split('-')              # tmp = 'signatures'
        query = "INSERT INTO Source_Table VALUES ( '{}', '{}')".format(str(library_name), str(version))
        cur.execute(query)

        query = "SELECT rowid FROM Source_Table WHERE library_name = '{}' and version = '{}' LIMIT 1;".format(library_name, version)
        for row in cur.execute(query):
            source_id = row[0]              # primary key of Source_Table library entry

        with open(sigs_path + every_file) as file:
            for line in file:
                line = line[:-1]    #removing trailing character
                library, unqhash = line.split(":")
                query = "INSERT INTO Child_Table VALUES ( '{}', '{}', '{}')".format(str(library), str(unqhash), source_id)
                cur.execute(query)
            

if __name__ == "__main__":
    global conn, cur
    print("Enter the path of the database: ")
    #path = str(input())
    path = "/Users/gilf0ile/3xpwn/project/dir/scripts/database.db"
    print(path)
    try:
        conn = sqlite3.connect(path)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            cur = conn.cursor()
            print("-> Database Connected")

    create_table("Source_Table")
    create_table("Child_Table")
    transfer()
    print_table("Source_Table")

    conn.commit()
    conn.close()
