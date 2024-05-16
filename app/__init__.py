from flask import Flask,request,session,jsonify,g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DevelopmentConfig
from model.database.db import db,User
import os
# 全局对象初始化
migrate = Migrate()
login_manager = LoginManager()
class CustomError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig) 

    app.secret_key = 'ylTIJL_jvzCHlSeKj5dH_MXj'

    db.init_app(app)
    migrate = Migrate(app, db) 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from model.database.db import User 
        return User.query.get(int(user_id))

    # 蓝图注册
    from .routes import main as main_blueprint, auth as auth_blueprint
    from app.controller.login.login import lg
    from app.controller.indexcontroller import upload
    from app.controller.userController import userinfo
    from app.controller.indexcontroller import serch
    from app.controller.indexcontroller import board,article,select
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(lg)
    app.register_blueprint(userinfo)
    app.register_blueprint(upload)
    app.register_blueprint(serch)
    app.register_blueprint(board)
    app.register_blueprint(article)
    app.register_blueprint(select)
    app.config['photopath']=os.path.join(os.getcwd(),'app','static','photo')
    if not os.path.exists(app.config['photopath']):
        os.mkdir(app.config['photopath'])
    @app.before_request
    def sessionlogin():
        routelist=['/userinfo','/upload.html','/blogupload','/search','/comment/add','/getuser','/like']
        path=request.path
        if path in routelist:
           username=session.get('username')
           if username is None:
               raise CustomError("请登录重试", status_code=403)
           user=User.query.filter_by(username=username).first()
           if  user is None:
               raise CustomError("请登陆后重试", status_code=403)
           g.userObject=user
    @app.errorhandler(CustomError)
    def handle_custom_error(error):
      
        response = jsonify({"error":str(error),'code':403})
        response.status_code = 403
        session.clear()

        return response
    return app

