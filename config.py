import os

class Config:
    # SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL")
    MAIL_PASSWORD = os.getenv("PASSWORD")
    # CKEDITOR_PKG_TYPE = 'full' 
    CKEDITOR_CONFIG = {
        'versionCheck': False
    }
