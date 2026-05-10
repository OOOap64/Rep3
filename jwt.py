import flask_bcrypt
from flask_bcrypt import *
from flask import *
from flask_jwt_extended import *
import sqlite3 as sql 
from flask_sqlalchemy import *
import flask_jwt_extended
app=Flask(__name__)
app.config['SECRET_KEY']='your_strong_secret_key'
app.config['JWT_SECRET_KEY']='your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION']=['headers']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)
jwt=flask_jwt_extended.JWTManager(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    cart = db.Column(JSON, nullable=True, default=list)  # Make cart nullable

    # Define the relationship between User and CartProducts
    cart_products = relationship('CartProducts', backref="user", lazy="dynamic")
    # Define the relationship between User and Wishlists
    wishlists = db.relationship('Wishlists', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
def connect_db():
    conn=sql.connect("database.db")
    cur=conn.cursor()
    cur.execute("""IF NOT EXIST Users( id int primary key,
                 name varchar(25), 
                 password varchar(50),
                 group varchar(5),
                 post varchar(20),
                device varchar(100));""")
    # cur.execute("INSERT INTO ")
    conn.commit()
    cur.execute("""IF NOT EXIST Tasks( id int primary key,
                 descriptions varchar(25), 
                 executer varchar(25));""")
    # cur.execute("INSERT INTO ")
    conn.commit()
    return 
@app.route('/git_name', methods=['GET'])
@jwt_required()
def get_name():
    us_id=get_jwt_identity()
    user=User.query.filter_by(id=us_id).first()
    if user:
        return jsonify({'message':'Userfound', 'name':user.name})
    else:
        return jsonify({'message':'User not found'}), 404
@app.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    us_nm=data['username']
    us_pw=data['password']
    user=User.query.filter_by(username=us_nm).first()
    if user in flask_bcrypt.bcrypt.check_passowrd_hash(user.password, us_pw):
        access_tkn=create_access_token(identity=user.id)
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401
    
if __name__=="__main__":
    with app.app_context():
        app.run(debug=True)
# import sqlalchemy as sqlalm# import *
# import SQLAlchemy
# sqlalm.SQ
# app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URL']='sqlite:///site.db'
# db=SQLAlchemy(app)
# class User 






# import jwt 
# from flask import *#Flask, request, jsonify, make_response
# import datetime 

# app=Flask(__name__)
# app.config['secret_key']="this is secret"

# def token_req(f):
#     def decorated(*args, **kwargs):
#         tkn=request.args.get('get')
#         if not tkn: 
#             return jsonify({'error':'token is missing'}), 403
#         try:
#             jwt.decode(tkn, app.config['secret_key'], algorithms="HS256")
#         except Exception as err:
#             return jsonify({'error':'token is invalid/expired'})
#         return f(*args, **kwargs)
#     return decorated

# @app.route("/login")
# def login():
#     auth=request.authorization 
#     print(auth)
#     if auth and auth.password=="password":
#         tkn=jwt.encode({'user':auth.username, 
#                         'exp':datetime.datetime.utcnow()\
#                         +datetime.timedelta(seconds=10)},
#                         app.config['secret_key'])
#         return f'<a href="http:localhost:5000/access?token={tkn}"> Private link</a>'
#     return make_response('Could you verify', 401, {'WWW-Authenticate':'Basic realm="Login Required"'}) 

# @app.route("/access")
# @token_req
# def access():
#     return jsonify({'message':'valid jwt token'})

# if __name__=="__main__":
#     app.run()    