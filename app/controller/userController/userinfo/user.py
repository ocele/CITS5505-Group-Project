from app.controller.userController.blueprint import userinfo
from flask import render_template,session,redirect,request,jsonify,current_app,g
from model.database.db import User,db
import time,os
@userinfo.route('/userinfo', methods=['GET'])
def get_userinfo():
    username=session.get('username')
    if username is None:
        session.clear()
        return redirect('/login')
    user=User.query.filter_by(username=username).first()
    if user is None:
        session.clear()
        return redirect('/login')
    return render_template('profile.html',data=user)
@userinfo.route('/userinfo',methods=['POST'])
def upuser():
    username=session.get('username')
    filebool=False
    passwordbool=False
    password=request.form.get('password')
    file=request.files.get('file')
    user=User.query.filter_by(username=username).first()
    if file is not None:
        filebool=True
       
        filename=str(time.time())+'.png'
        path=os.path.join(current_app.config['photopath'],filename)
        file.save(path)
        if user.photopath!='default.png':
           os.remove(os.path.join(current_app.config['photopath'],user.photopath))
        user.photopath=filename
        db.session.commit()
    if password is not None:
        user.password=password
        db.session.commit()
        passwordbool=True
    if passwordbool or filebool:
        return jsonify(code=200,message='更改成功')
    return jsonify(code=400,message='无效请求')
        
@userinfo.route('/getuser',methods=['GET'])
def getuser():
    userObject=g.get('userObject')
    return jsonify({'username':userObject.username,'photo':'/static/photo/'+userObject.photopath,'code':200})
