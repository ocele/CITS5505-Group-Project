from app.controller.indexcontroller.blueprint import select
from model.database.db import Article,User
from flask import request,jsonify
from sqlalchemy import desc,asc
import html
@select.route('/article/sort',methods=['POST'])
def articlesort():
        value=request.get_json().get('value')
        if not (value==1 or value==0):
            return jsonify({'code':400,'msg':'参数错误'})
        if value==1:
            articlesdata = Article.query.order_by(desc(Article.create_time)).all()
        else:
            articlesdata = Article.query.order_by(asc(Article.create_time)).all()
        data=[]
        for i in articlesdata:
             data.append(dict(content=html.escape(i.content),title=html.escape(i.title),create_time=i.create_time.strftime("%Y-%m-%d %H:%M:%S"),id=i.id,url='./article?id='+str(i.id)))
        return jsonify(code=200,data=data)
   
