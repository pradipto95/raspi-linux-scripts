import sqlite3
import requests
import datetime
import json

def sync():
    ns=0
    s1=0
    flag=0
    delr=0
    invd=0
    conn=sqlite3.connect('att.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs(synced varchar,notsynced varchar,deleted varchar,invalid varchar,sync_time varchar)''')
    c.execute('''select * from attendance where status=0''')
    for i in c.fetchall():
        if i[4]:
            now = datetime.datetime.now()
            ntime = now.strftime("%H")
            #o={'st_id':i[1],'date':i[2],'out_time':i[4],'duration':i[5],'status':'0','notif_s':'1'}
            if int(ntime)>=13:
                o={'st_id':i[1],'date':i[2],'out_time':i[4],'duration':i[5],'status':'1','notif_s':'1'}
            else:
                o={'st_id':i[1],'date':i[2],'out_time':i[4],'duration':i[5],'status':'0','notif_s':'1'}
            flag=1
            se = requests.session()
            response = se.post(url="https://attendanceproject.herokuapp.com/home/apia/",data=o)
            #response = se.post(url="http://127.0.0.1:8000/home/apia/",data=o)
            print(response.content)
            try:
                json_data = json.loads(response.content)
            except:
                continue
            http_msg=''
            http_sid=''
            try:
                http_sid=json_data["st_id"]
            except KeyError:
                http_msg=json_data["msg"]
            if http_sid:
                s1=s1+1
                print('Record Deleted as Synced(Leave time present)')
                c.execute('''DELETE FROM attendance WHERE std_id=?''',(i[1],))
                delr=delr+1
                conn.commit()
            if http_msg:
                print(http_msg)
                ns=ns+1

        elif i[6]=='0':
            t={'st_id':i[1],'date':i[2],'in_time':i[3],'status':'1','notif_s':'1'}
            se = requests.session()
            response = se.post(url="https://attendanceproject.herokuapp.com/home/apia/",data=t)
            #response = se.post(url="http://127.0.0.1:8000/home/apia/",data=t)
            try:
                json_data = json.loads(response.content)
            except:
                continue
            print(response.content)
            flag=1
            http_msg=''
            http_sid=''
            try:
                http_sid=json_data["st_id"]
            except KeyError:
                http_msg=json_data["msg"]
            if http_sid:
                print("Status bit changed")
                c.execute('''UPDATE attendance SET status=? WHERE std_id=?''',('1',i[1]))
                conn.commit()
                s1=s1+1
            if http_msg:
                print("Invalid Admission ID so record deleted")
                c.execute('''DELETE FROM attendance WHERE std_id=?''',(i[1],))
                conn.commit()
                invd=invd+1
    if flag==1:
        now = datetime.datetime.now()
        time=now.strftime("%H:%M:%S")
        c.execute('''INSERT INTO logs values(?,?,?,?,?)''',(str(s1),str(ns),str(delr),str(invd),time))
        conn.commit()
        c.execute('''SELECT * FROM logs''')
        print(c.fetchall())
    conn.close()  
sync()
