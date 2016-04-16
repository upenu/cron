# Make sure to run this inside virtualenv

import datetime
from   dateutil.parser import parse
import facebook
import MySQLdb
import os

def get_fb():
    direc = os.path.dirname(__file__)
    fb_data = os.path.join(direc, '../facebook_data')
    with open(fb_data, 'r') as f:
        token = f.read().strip()
    graph = facebook.GraphAPI(access_token=token, version="2.6")

    result = graph.get_object(id="/ucbupe/events", fields="name,start_time,description,place,cover,id")
    return result['data']

def get_db(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM upe_calendar_event;")
    db_results = cur.fetchall()
    cur.close()

    return db_results

def put_db(conn, entry, exists):
    cur = conn.cursor()
    if not exists:
        cur.execute(u"""INSERT INTO upe_calendar_event (name, start_time, description, location, banner, facebookid)
                    VALUES (%(name)s, %(start_time)s, %(description)s, %(location)s, %(banner)s, %(facebookid)s);""",
                    entry)
    else:
        cur.execute(u"""UPDATE upe_calendar_event
                    SET name=%(name)s,start_time=%(start_time)s,description=%(description)s,location=%(location)s,banner=%(banner)s
                    WHERE facebookid = %(facebookid)s;""",
                    entry)

    cur.close()

conn = MySQLdb.connect(host="localhost", user="admin", passwd="littlewhale", db="upe_db", port=3306)
conn.set_character_set('utf8')

db = get_db(conn)
fb = get_fb()

for fbe in fb:
    start = parse(fbe["start_time"])
    fbe_t = {
             "name" : fbe["name"],
             "start_time" : start,
             "description" : fbe["description"] if "description" in fbe else "",
             "location" : fbe["place"]["name"],
             "banner" : fbe["cover"]["source"] if "cover" in fbe else "",
             "facebookid" : fbe["id"]
            }
    for dbe in db:
        if dbe[6] == int(fbe_t["facebookid"]):
            # Match found
            put_db(conn, fbe_t, True)
            break
    else:
        # No match found
        put_db(conn, fbe_t, False)
        pass

conn.commit()
conn.close()

