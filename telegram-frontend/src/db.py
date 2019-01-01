import psycopg2
import os
import constants as c

try:
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(host=os.environ["POSTGRES_HOST"],database="postgres", user="postgres", password=os.environ["POSTGRES_PASSWORD"])
except (Exception, psycopg2.DatabaseError) as error:
    print(error)

def iter_row(cursor, size=100):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def get_authorized_users():
    try:
        cur = conn.cursor()
        auth = []
        cur.execute("SELECT id, authorized FROM users")
        for row in iter_row(cur):
                    if (row[1]):
                        auth.append(row[0])
        cur.close()
        return auth
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_authorized(id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE id ="+ str(id)+" AND authorized = true")
        if not cur.fetchone():
            cur.close()
            return False
        else:
            cur.close()
            return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
def add_user(id, username, name):
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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if(c.DEBUG>0):
        if created:
            print("Registered: "+ username+ " with id: "+ str(id))
        else:  
            print("Already registered: "+ username+ " with id: "+ str(id))
    return created

def subscribe(user_id, gate_id):
    sql = """INSERT INTO public.subscriptions(user_id, gate_id) VALUES (%s, %s)"""
    created = False
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM subscriptions WHERE user_id =" + str(user_id) + " AND gate_id ="+ str(gate_id))
        if not cur.fetchone():
            cur.execute(sql, (user_id, gate_id))
            conn.commit()
            created = True
        else:
            created =  False
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    if(c.DEBUG>0):
        if created:
            print("Subscribed: "+ str(user_id)+ " with gate: "+ str(gate_id))
        else:  
            print("Already subscribed: "+ str(user_id)+ " with gate: "+ str(gate_id))
    return created