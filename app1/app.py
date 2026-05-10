import sqlite3 as sql
import socket
#Groups: A, B, C
#Posts: Backend, Frontend, DevOps, TeamLead, DataScientist

con=sql.connect("sqlite.db")
cur=con.cursor()
cur.execute("""CREATE TABLE Users (
            id int primary key,
            name varchar(80),
            password varchar(80),
            post varchar(80),
            grp varchar(80),
            device varchar(80));""")
con.commit()    
cur.execute("""CREATE TABLE Tasks (
            id int primary key,
            task varchar(200),
            executer varchar(80));""")
con.commit() 
cur.close()   
con.close()
# def conn():
#     con=sql.connect("sqlite.db")
#     return con.cursor()
# cur=conn()
# cur.execute("SELECT 67*7;")
# print(cur.fetchone())

print(socket.gethostname())
# if __name__=='__main__':
#     app.run()
