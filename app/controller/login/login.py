from flask import Blueprint,request,session,jsonify
from model.database.db import db,User
import time
lg=Blueprint('lg',__name__)
@lg.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    try:
        username=data['username']
        password=data['password']
    except KeyError:
        return jsonify(code=400,message='请求错误')
    finduser=User.query.filter_by(username=username).first()
    if finduser is None:
        return jsonify(code=400,message='用户不存在')
    if finduser.password!=password:
        return jsonify(code=400,message='密码错误')
    session['userid']=finduser.id
    session['username']=finduser.username
    session['timestamp']=time.time()
    return jsonify(code=200,message='登录成功')
