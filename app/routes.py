
from flask import Blueprint, render_template, request, redirect, url_for,jsonify,session
from flask_login import logout_user, login_required
from .forms import RegistrationForm, LoginForm
from model.database.db import  db,User,Article
from sqlalchemy.exc import  IntegrityError
from flask import flash
import time
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/')
def index():
    tasks=[]
    articledata=Article.query.join(User).filter(Article.userid == User.id).all()  
    for i in articledata:
       
        tasks.append({'id':i.id,'title':i.title,'content':i.content,'time':i.create_time.strftime("%Y-%m-%d %H:%M")})
    return render_template('index.html',tasks=tasks)

@main.route('/login')
def main_login():
    type = request.args.get('type', default=1, type=int)
    return render_template('login.html', type=type)

@main.route('/forgot_password')
def forgot_password():
    return render_template('password.html')

@auth.route('/register', methods=['GET', 'POST'])
def app_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data,password=form.password.data)
        
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return jsonify({'message': '用户名或邮箱已存在','code':400})
        session['username']=user.username
        session['userid']=user.id
        session['timestamp']=time.time()
        return redirect('./')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(form, field).label.text}: {error}', 'error') 
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index')) 
