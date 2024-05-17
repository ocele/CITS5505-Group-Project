# Clean up testdata
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from model.database.db import db, User, Article, Comment, Articlelike 
from app import create_app

app = create_app()
app.app_context().push()

def delete_test_data():
    try:
        user_count = db.session.query(User).count()
        article_count = db.session.query(Article).count()
        comment_count = db.session.query(Comment).count()
        articlelike_count = db.session.query(Articlelike).count()

        print(f"Before deletion: {user_count} users, {article_count} articles, {comment_count} comments, {articlelike_count} articlelikes")

        db.session.query(Comment).delete()
        db.session.query(Articlelike).delete()
        db.session.query(Article).delete()
        db.session.query(User).delete()

        
        db.session.commit()

        user_count = db.session.query(User).count()
        article_count = db.session.query(Article).count()
        comment_count = db.session.query(Comment).count()
        articlelike_count = db.session.query(Articlelike).count()

        print(f"After deletion: {user_count} users, {article_count} articles, {comment_count} comments, {articlelike_count} articlelikes")

        print("Test data deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    delete_test_data()
