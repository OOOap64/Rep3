from flask import *
import json
import flask_jwt_extended

from flask_jwt_extended import *
# import jsonify
items=[]
with open("datas.json", 'r') as file:
    items=json.load(file)
app=Flask(__name__)
app.config["JWT_SECRET_KEY"]="123456"
jwt=flask_jwt_extended.JWTManager(app)

users={
    "admin":"password"
}

@app.route('/login', methods=["POST"])
def login():
    us_nm=request.json.get("username", None)
    us_pw=request.json.get("passowd", None)

    if us_nm not in users or users[us_nm]!=us_pw:
        return jsonify({"Message":"Credentials"})
    access_tkn=create_access_token(identity=us_nm)
    return jsonify(access_tkn)

@app.route("/items", methods=["GET"])
@jwt_required()
def get():
    return jsonify(items)

if __name__=="__main__":
    app.run( host="0.0.0.0", port="3000")