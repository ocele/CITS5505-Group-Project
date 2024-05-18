from app.controller.userController.blueprint import userinfo
from flask import render_template, session, redirect, request, jsonify, current_app, g
from model.database.db import User, db, Article, Comment
import time, os


@userinfo.route('/userinfo', methods=['GET'])
def get_userinfo():
    username = session.get('username')
    if username is None:
        session.clear()
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    if user is None:
        session.clear()
        return redirect('/login')
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


def get_articles_with_comments_from_user(user_id):
    user_comments = Comment.query.filter_by(userid=user_id).all()

    articles = [comment.article for comment in user_comments]

    distinct_articles = list(set(articles))

    return distinct_articles


@userinfo.route('/userinfo', methods=['POST'])
def upuser():
    username = session.get('username')
    filebool = False
    passwordbool = False
    password = request.form.get('password')
    file = request.files.get('file')
    user = User.query.filter_by(username=username).first()
    if file is not None:
        filebool = True

        filename = str(time.time()) + '.png'
        path = os.path.join(current_app.config['photopath'], filename)
        file.save(path)
        if user.photopath != 'default.png':
            os.remove(os.path.join(current_app.config['photopath'], user.photopath))
        user.photopath = filename
        db.session.commit()
    if password is not None:
        user.password = password
        db.session.commit()
        passwordbool = True
    if passwordbool or filebool:
        return jsonify(code=200, message='Update Successful')
    return jsonify(code=400, message='Request Denied')


@userinfo.route('/getuser', methods=['GET'])
def getuser():
    userObject = g.get('userObject')
    return jsonify({'username': userObject.username, 'photo': '/static/photo/' + userObject.photopath, 'code': 200})
