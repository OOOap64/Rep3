
import socket
from flask import *
from markupsafe import * 
# import psycopg2 as pst
import sqlite3 as sql
#Groups: A, B, C
#Posts: Backend, Frontend, DevOps, TeamLead, DataScientist
app=Flask(__name__, static_folder="static")
def conn():
    con=sql.connect("sqlite.db")
    cur=con.cursor()
    return cur, con

@app.route("/add_task")#, methods=["POST"])
def add_task():
    return render_template("add_task.html")

@app.route("/")#, methods=["POST"])
def reg():
    
    return render_template("index.html")

@app.route("/add_task", methods=["POST"])
def post_reg():
    cur, con=conn()
    cur.execute("SELECT device FROM Users")
    dev1=cur.fetchone()
    dev=socket.gethostname()
    print(dev1)
    if dev1[0][0]!=dev :
        print("AAAAAA")
    res=request.json()
    print(res) 
    

@app.route("/home")#, methods=["POST"])
def ui():
    return render_template("UI.html")


if __name__=="__main__":
    app.run(debug=True)