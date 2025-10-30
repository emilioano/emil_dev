import sqlite3

DBPath = 'db.db'


def createdb():
    # Creating DB if not already existing
    CreateDB = sqlite3.connect(DBPath)
    CreateDB.close()

def createtable(tablename):
    #Create table
    CreateTable = sqlite3.connect(DBPath)
    cursor = CreateTable.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tablename} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        time TEXT, 
        ip TEXT, 
        location TEXT, 
        mood TEXT, 
        genre TEXT, 
        airesult TEXT, 
        musicresult TEXT)''')

    CreateTable.commit()
    CreateTable.close()

def dbquery(tablename):
    # DB query
    DBQuery = sqlite3.connect(DBPath)
    cursor = DBQuery.cursor()

    cursor.execute(f'''SELECT * FROM {tablename}''')

    fetchrows = cursor.fetchall()

    for i in fetchrows:
        pass
    print(fetchrows)

    DBQuery.close()

def dbinsert(tablename):
    # DB Insert
    DBInsert = sqlite3.connect(DBPath)
    cursor = DBInsert.cursor()

    cursor.execute(f'''

    INSERT INTO {tablename} (time, ip, location, mood, genre, airesult, musicresult)
    VALUES('1','2','3','4','5','6','7')

    ''')

    DBInsert.commit()
    DBInsert.close()

def deletetable():
    # Table deletion
    TableDel = sqlite3.connect(DBPath)
    cursor = TableDel.cursor()

    cursor.execute('''

    DROP TABLE requests

    ''')

    TableDel.commit()
    TableDel.close()

def dbupdate(tablename):
    # DB Update
    DBInsert = sqlite3.connect(DBPath)
    cursor = DBInsert.cursor()

    cursor.execute(f'''

    UPDATE {tablename} SET time = '2025-09-24 19:12:30' WHERE genre = 'Ska punk'

    ''')

    DBInsert.commit()
    DBInsert.close()



def dbdelposts(tablename):
    # DB Update
    DBInsert = sqlite3.connect(DBPath)
    cursor = DBInsert.cursor()

    cursor.execute(f'''

    DELETE FROM {tablename}

    ''')

    DBInsert.commit()
    DBInsert.close()




dbquery('requests')