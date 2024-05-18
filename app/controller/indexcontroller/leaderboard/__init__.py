from flask import render_template, request
from model.database.db import User
from app.controller.indexcontroller.blueprint import board


@board.route('/leaderboard.html')
def leader():
    top_users = User.query.order_by(User.money.desc()).limit(10).all()

    return render_template('leaderboard.html', users=top_users)
