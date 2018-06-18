import sqlite3
import datetime
import time
conn = sqlite3.connect('att.db')
c = conn.cursor()

def db():
    start_time = time.time()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance(ID integer PRIMARY KEY,std_id varchar2,entry_date varchar2,entry_time varchar2,leave_time varchar2,duration varchar2,status varchar2)''')
    print("Enter the values to be inserted")
    print("Student ID")
    sid=input()
    std_id=sid
    t = (std_id,)
    c.execute('SELECT * FROM attendance where std_id=?',t)
    d=c.fetchone()
    if d:
        datetime_object = datetime.datetime.strptime(d[3],'%H:%M:%S')
        dtime=datetime_object.strftime("%H:%M:%S")
        FMT = "%H:%M:%S"
        now = datetime.datetime.now()
        ntime=now.strftime("%H:%M:%S")
        date = datetime.datetime.strptime(str(ntime), FMT) - datetime.datetime.strptime(str(dtime), FMT)
        tdelta = datetime.datetime.strptime(str(date),"%H:%M:%S")
        rtime=int(tdelta.hour)*60+int(tdelta.minute)+(int(tdelta.second)/60)
        if rtime>1:
            exit_att(std_id,d[3])
    else:
        now = datetime.datetime.now()
        ntime = now.strftime("%H")
        if int(ntime)>=13:
            exit_att_deafult(std_id)
        else:
            entry_att(std_id)
    printr()
    db()

    #c.execute('''drop table attendance''')
    #entry_att(std_id)
    #printr()
    #sync()
    #conn.close()
    #print(time.time()-start_time)


def entry_att(std_id):
    now = datetime.datetime.now()
    date=now.strftime("%d/%m/%y")
    time=now.strftime("%H:%M:%S")
    c.execute('''INSERT INTO attendance(std_id,entry_date,entry_time,status) values(?,?,?,?)''',(std_id,date,time,'0'))
    conn.commit()

def exit_att_deafult(std_id):
    now = datetime.datetime.now()
    date=now.strftime("%d/%m/%y")
    time=now.strftime("%H:%M:%S")
    duration="00:00:00"
    c.execute('''INSERT INTO attendance(std_id,entry_date,leave_time,duration,status) values(?,?,?,?,?)''',(std_id,date,time,duration,'0'))
    conn.commit()



def exit_att(std_id,ptime):
    now = datetime.datetime.now()
    ltime=now.strftime("%H:%M:%S")
    FMT = '%H:%M:%S'
    duration = datetime.datetime.strptime(str(ltime), FMT) - datetime.datetime.strptime(str(ptime), FMT)
    utime=datetime.datetime.strptime(str(duration),"%H:%M:%S")
    dtime=utime.strftime("%H:%M:%S")
    c.execute('''UPDATE attendance SET leave_time=?,duration=?,status=? where std_id=?''',(ltime,dtime,'0',std_id))
    conn.commit()


def printr():
    c.execute('''SELECT * FROM attendance''')
    print(c.fetchall())

#printr()
db()
