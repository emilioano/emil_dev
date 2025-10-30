import sqlite3
from datetime import datetime




DBPath = 'db/db.db'

def insertdbrecord(ip,location,mood,genre,airesult,musicresult):
    date_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print(f'DB adress: {DBPath}')
    SQLquery = sqlite3.connect(DBPath)
    cursor = SQLquery.cursor()

    SQLString = '''
    INSERT INTO requests (time, ip, location, mood, genre, airesult, musicresult)
    VALUES (?,?,?,?,?,?,?)
    '''

    cursor.execute(SQLString, (date_time_str,ip,location,mood,genre,airesult,musicresult))

    #print(f'SQL-sträng som körs: {SQLString}')

    SQLquery.commit()
    SQLquery.close()


def listdbrecords():
    SQLquery = sqlite3.connect(DBPath)
    cursor = SQLquery.cursor()

    SQLString = f'''
    SELECT * FROM requests ORDER BY time DESC
    '''
    cursor.execute(SQLString)
    fetchrows = cursor.fetchall()

    for row in fetchrows:
        #print(f'Rad: {row}\n')
        pass
    print(f'Resultat: {fetchrows}')
    SQLquery.close()
    return fetchrows