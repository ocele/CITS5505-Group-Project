class Config:
    SECRET_KEY = 'ylTIJL_jvzCHlSeKj5dH_MXj'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///yourdatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class Config:
    SECRET_KEY = 'your_secret_key'
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your-email@example.com'
    MAIL_PASSWORD = 'your-email-password'