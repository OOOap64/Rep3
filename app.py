from collections import *
import sqlite3 as sql
from flask import Flask, request, url_for, render_template, redirect, jsonify
import socket
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies
)
from flask_cors import CORS 
import datetime 
from flask_jwt_extended import set_access_cookies

app=Flask(__name__, static_folder="static")
app.config['JWT_SECRET_KEY']='super-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=datetime.timedelta(minutes=15)
app.config['JWT_TOKEN_LOCATION']=['cookies']
app.config['JWT_COOKIE_SECURE']=False 
app.config['JWT_COOKIE_HTTPONLY']=True 
app.config['JWT_COOKIE_SAMESITE']='Strict'
jwt=JWTManager(app)

def conn():
    con=sql.connect("sqlite.db")
    cur=con.cursor()
    return  con, cur

def none_to_0(i):
    if i is None:
        return 0
    return i
def none_to_0m(i):
    if i is None:
        return []
    return i

def access():
    hs=socket.gethostbyname(socket.gethostname())
    con, cur=conn()
    cur.execute(f"SELECT * FROM Users WHERE device='{hs}'")
    aa=cur.fetchall()
    cur.close()
    con.close()
    if aa is None:
        return render_template("index.html", err="You need to sign up for getting an access")

def is_teamlead():
    con, cur= conn()
    dev=socket.gethostbyname(socket.gethostname())
    cur.execute(f"SELECT post FROM Users where device='{dev}'")
    a=cur.fetchone()
    cur.execute(f"SELECT * FROM Users where device='{dev}'")
    aa=cur.fetchall()
    cur.close()
    con.close()
    if a[0]!="TeamLead":
        if dev not in aa:
            return redirect(url_for("reg_post"))
        return redirect(url_for("ui"))
@app.route("/", methods=["POST", "GET"])
def reg_post():
    err=""
    if request.method=="POST":
        con, cur=conn()
        host=str(socket.gethostbyname(socket.gethostname()))
        cur.execute("SELECT * from Users;")
        uss=cur.fetchall()
        hss=[p[-1] for p in uss]
        pws=[p[1] for p in uss]
        nms=[p[0] for p in uss]
        nm=request.form["name"]
        pw=request.form["password"]
        ps=request.form["post"]
        gp=request.form["grp"]
        if host not in hss:
            cur.execute(f"SELECT post from Users WHERE grp='{gp}';")
            us_gr=cur.fetchall()
            pss=Counter([p[2] for p in uss])
            if len(nm)>4 and len(pw)>4 and pw not in pws and nm not in nms:
                if none_to_0(pss.get("TeamLead"))<2 and ps=="TeamLead" or "TeamLead" not in pss :
                    access_tkn=create_access_token(identity=nm)
                    refresh_tkn=create_refresh_token(identity=nm)
                    cur.execute(f"""INSERT INTO Users(id, name, password, post, grp, device)
                    VALUES({len(uss)+1}, '{nm}', '{pw}', '{ps}', '{gp}', '{host}');""")
                    con.commit()
                    cur.close()
                    con.close()
                    rps=jsonify({"msg":"Successful"})
                    set_access_cookies(access_tkn)
                    set_refresh_cookies( refresh_tkn)
                    return redirect(url_for('ui'))
            err=f"Wrong print"
        else:
            cur.execute(f"SELECT * FROM Users WHERE device='{str(host)}'")
            cc=cur.fetchall()
            dt=cc[0]
            if dt[1]==nm and pw==dt[2] and ps==dt[3] and gp==dt[4]:
              asc_tkn=create_access_token(identity=nm)
              ref_tkn=create_refresh_token(identity=nm)
              rps=jsonify({'msg':'Successful'})
              set_access_cookies(rps, asc_tkn)
              set_refresh_cookies(rps, ref_tkn)

              return redirect(url_for('ui'))
        err=f"Wrong print"

        cur.close()
        con.close()    
    return render_template("index.html", err=err)

@app.route("/add_task", methods=["POST", "GET"])
# @jwt_required
def post_reg():
    con, cur=conn()
    dev=socket.gethostbyname(socket.gethostname())
    cur.execute(f"SELECT * FROM Users where device='{dev}'")
    dev1=cur.fetchone()
    cur.execute("SELECT * FROM Tasks")
    task=cur.fetchall()
    cur.execute(f"SELECT * FROM Users where grp='{dev1[-2]}'")
    uss=cur.fetchall()
    if request.method=="POST":
        res=request.form
        if dev1[3]=="TeamLead":
            cur.execute(f"INSERT INTO Tasks(id, task, executer, types, grp) VALUES({len(task)+1}, '{res["task"]}', '{res["executer"]}', NULL, '{dev1[-2]}');")
            con.commit()
        cur.close()
        con.close() 
        return redirect(url_for('ui'))
    return render_template("add_task.html", uss=uss)   

@app.route("/home")#, methods=["POST"])
@jwt_required()
def ui():
    con, cur=conn()
    dev=socket.gethostbyname(socket.gethostname())
    cur.execute(f"SELECT * FROM Users where device='{dev}'")
    dev1=cur.fetchone()
    cur.execute(f"SELECT * FROM Users WHERE grp='{dev1[-2]}'")
    us=cur.fetchall()
    print(us)
    cur.execute(f"SELECT * FROM Tasks  WHERE grp='{dev1[-2]}' and types is NULL ")
    tsk1=cur.fetchall()
    cur.execute(f"SELECT * FROM Tasks  WHERE grp='{dev1[-2]}' and types='a'")
    tsk2=cur.fetchall()
    cur.execute(f"SELECT * FROM Tasks WHERE grp='{dev1[-2]}' and types='b'")
    tsk3=cur.fetchall()
    cur.close()
    con.close()
    nm=get_jwt_identity()
    return render_template("UI.html", 
                           nm=nm,
                           dev1=dev1,
                           us=none_to_0m(us), 
                           tsk=none_to_0m(tsk1),
                           tsk2= none_to_0m(tsk2), 
                           tsk3= none_to_0m(tsk3))


@app.route("/transform/<int:id>")
def tran(id):
    is_teamlead()
    con, cur=conn()
    cur.execute(f"UPDATE Tasks SET types='a' WHERE id={id};")
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for("ui"))

@app.route("/transform1/<int:id>")
def tran1(id):
    is_teamlead()
    con, cur=conn()
    cur.execute(f"UPDATE Tasks SET types='b' WHERE id={id};")
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for("ui"))
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    is_teamlead()
    dev=socket.gethostbyname(socket.gethostname())
    cur.execute(f"SELECT * FROM Users where device='{dev}'")
    dev1=cur.fetchone()
    cur.execute(f"SELECT * FROM Users where grp='{dev1[-2]}'")
    uss=cur.fetchall()
    if request.method=="POST":
        tsk=request.form["task"]
        e=request.form["executer"]
        con, cur=conn()
        cur.execute(f"UPDATE Tasks SET task='{tsk}', executer='{e}' WHERE id={id} ;")
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for("ui"))
    return render_template("add_task.html", uss=uss)

@app.route("/delete/<int:id>")
def delete(id):
    is_teamlead()
    con, cur=conn()
    cur.execute(f"DELETE FROM Tasks WHERE id={id} ;")
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for("ui"))

if __name__=="__main__":
    app.run(debug=True, port="5000")