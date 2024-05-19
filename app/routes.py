import os

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from .forms import RegistrationForm, LoginForm
from model.database.db import db, User, Article, Comment
from sqlalchemy.exc import IntegrityError
from flask import flash
import time
from functools import wraps

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)


def my_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'userid' not in session or 'username' not in session:
            return jsonify(code=401, message='Login Required')
        return func(*args, **kwargs)

    return wrapper


@main.route('/')
def index():
    users = User.query.order_by(User.money.desc()).all()
    return render_template('leaderboard.html', users=users)


@main.route('/index')
def index_page():
    tasks = []
    articledata = Article.query.join(User).filter(Article.userid == User.id).order_by(Article.create_time.desc()).all()
    for i in articledata:
        tasks.append(
            {'id': i.id, 'title': i.title, 'content': i.content, 'time': i.create_time.strftime("%Y-%m-%d %H:%M")}
        )
    return render_template('index.html', tasks=tasks)


@main.route('/login')
def main_login():
    type = request.args.get('type', default=1, type=int)
    return render_template('login.html', type=type)


@main.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username=current_user.username)
    else:
        return redirect(url_for('main_login'))


@main.route('/forgot_password')
def forgot_password():
    return render_template('password.html')


@auth.route('/register', methods=['GET', 'POST'])
def app_register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'code': 400, 'message': 'Please provide all required fields.'}), 200

        if User.query.filter_by(username=username).first():
            return jsonify({'code': 400, 'message': 'User Name Has Been Taken.'}), 200

        if User.query.filter_by(email=email).first():
            return jsonify({'code': 400, 'message': 'Email already exists.'}), 200

        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        session['userid'] = new_user.id
        session['timestamp'] = time.time()

        return jsonify({'code': 200, 'message': 'User registered successfully.'}), 200
    else:
        return render_template('register.html')


@main.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('timestamp', None)
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    sort_order = request.form.get('sortOrder')

    query = Article.query.filter(Article.title.contains(keyword) | Article.content.contains(keyword))

    if sort_order == 'date-newest':
        query = query.order_by(Article.create_time.desc())
    elif sort_order == 'date-oldest':
        query = query.order_by(Article.create_time.asc())

    tasks = query.all()

    results = [
        {'id': task.id, 'title': task.title, 'content': task.content,
         'time': task.create_time.strftime("%Y-%m-%d %H:%M")}
        for task in tasks
    ]

    return render_template('index.html', tasks=results, word=keyword，sort_order=sort_order)


def get_articles_with_comments_from_user(user_id):
    user_comments = Comment.query.filter_by(userid=user_id).all()

    # 获取这些评论相关的文章
    articles = [comment.article for comment in user_comments]

    # 对文章列表进行去重处理
    distinct_articles = list(set(articles))

    return distinct_articles


@main.route('/userinfo', methods=['GET', 'POST'])
@my_login_required
def userinfo():
    username = session.get('username')
    if username is None:
        session.clear()
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    if user is None:
        session.clear()
        return redirect('/login')
    if request.method == 'POST':
        password = request.form.get('password')
        file = request.files.get('file')
        user = User.query.get(session['userid'])
        if password:
            user.password = password
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('app/static/photo', filename))
            print(filename)
            user.photopath = filename
        db.session.commit()

        return jsonify({'code': 200, 'message': 'Update successful'})
    else:
        tasks = []
        userid = session.get('userid')
        articledata = Article.query.filter_by(userid=userid).all()
        answers_articles = get_articles_with_comments_from_user(userid)
        answers = []
        for i in articledata:
            tasks.append(
                {'id': i.id, 'title': i.title, 'content': i.content, 'time': i.create_time.strftime("%Y-%m-%d %H:%M"),
                 'user': i.user.username})
        for i in answers_articles:
            answers.append(
                {'id': i.id, 'title': i.title, 'content': i.content, 'time': i.create_time.strftime("%Y-%m-%d %H:%M"),
                 'user': i.user.username})
        return render_template('profile.html', data=user, tasks=tasks, answers=answers)


@main.route('/add', methods=['POST'])
@my_login_required
def add_task():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    task = Article(title=title, content=content, userid=session['userid'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'code': 200, 'message': 'Task added successfully'})
