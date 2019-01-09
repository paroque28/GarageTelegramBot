import psycopg2
import os
import constants as c

def connect():
    try:
        conn = psycopg2.connect(host=os.environ["POSTGRES_HOST"],database="postgres", user="postgres", password=os.environ["POSTGRES_PASSWORD"])
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def get_connection():
        return connect()

def iter_row(cursor, size=100):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def get_authorized_users():
    conn = get_connection()
    try:
        cur = conn.cursor()
        auth = []
        cur.execute("SELECT id, authorized FROM users")
        for row in iter_row(cur):
                    if (row[1]):
                        auth.append(row[0])
        cur.close()
        conn.close()
        return auth
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
#TODO: logic in query
def get_authorized(id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE id ="+ str(id)+" AND authorized = true")
        if not cur.fetchone():
            cur.close()
            conn.close()
            return False
        else:
            cur.close()
            conn.close()
            return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
def add_user(id, username, name):
    conn = get_connection()
    sql = """INSERT INTO users(id, username, name, authorized, role) VALUES (%s, %s, %s, false, 'stranger')"""
    created = False
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE id =" + str(id))
        if not cur.fetchone():
            cur.execute(sql, (id,username, name))
            conn.commit()
            created = True
        else:
            created =  False
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if(c.DEBUG>0):
        if created:
            print("Registered: "+ username+ " with id: "+ str(id))
        else:  
            print("Already registered: "+ username+ " with id: "+ str(id))
    return created

def subscribe(user_id, gate_id, typed):
    conn = get_connection()
    sql = """INSERT INTO public.subscriptions(user_id, gate_id, type) VALUES (%s, %s, %s)"""
    created = False
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM subscriptions WHERE user_id =" + str(user_id) + " AND gate_id ="+ str(gate_id))
        if not cur.fetchone():
            cur.execute(sql, (user_id, gate_id, typed))
            conn.commit()
            created = True
        else:
            created =  False
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if(c.DEBUG>0):
        if created:
            print("Subscribed: "+ str(user_id)+ " with gate: "+ str(gate_id) +" with type " +typed)
        else:  
            print("Already subscribed: "+ str(user_id)+ " with gate: "+ str(gate_id))
    return created
def unsubscribe(user_id, gate_id):
    conn = get_connection()
    sql = """DELETE FROM public.subscriptions WHERE user_id=%s AND  gate_id=%s"""
    created = False
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM subscriptions WHERE user_id =" + str(user_id) + " AND gate_id ="+ str(gate_id))
        if cur.fetchone():
            cur.execute(sql, (user_id, gate_id))
            conn.commit()
            created = True
        else:
            created =  False
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if(c.DEBUG>0):
        if created:
            print("Unsubscribed: "+ str(user_id)+ " with gate: "+ str(gate_id))
        else:  
            print("Already unsubscribed: "+ str(user_id)+ " with gate: "+ str(gate_id))
    return created

def get_subscribers(gate_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        auth = []
        cur.execute("""SELECT user_id FROM subscriptions WHERE gate_id = %s""", (gate_id,))
        result = list(iter_row(cur))
        cur.close()
        conn.close()
        return [item for sublist in result for item in sublist]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_subscribtions(user_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        auth = []
        cur.execute("""SELECT gate_id FROM subscriptions WHERE user_id = %s ORDER BY gate_id""", (user_id,))
        result = list(iter_row(cur))
        cur.close()
        conn.close()
        return [item for sublist in result for item in sublist]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
def add_event(id_event):
    conn = get_connection()
    sql = """INSERT INTO events(id) VALUES (%s)"""
    try:
        cur = conn.cursor()
        cur.execute(sql, (id_event))
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if(c.DEBUG>1):
        print("Event logged id: "+ str(id_event))
def get_events(num):
    conn = get_connection()
    try:
        cur = conn.cursor()
        auth = []
        cur.execute("""SELECT gate_id, event_id, logged_time FROM subscriptions ORDER BY logged_time DESC LIMIT %s""", (num,))
        result = list(iter_row(cur))
        cur.close()
        conn.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)