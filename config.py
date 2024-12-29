import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///site.db")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No SQLALCHEMY_DATABASE_URI set for Flask application")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL")
    MAIL_PASSWORD = os.getenv("PASSWORD")

    # CKEDITOR_CONFIG = {
    #     'versionCheck': False,
    #     'height': 300,
    #     'toolbar': 'Full',
    #     'removePlugins': 'elementspath'
    # }

    # Allowed tags and attributes for sanitization
    ALLOWED_TAGS = [
        'b', 'i', 'u', 'a', 'p', 'ul', 'ol', 'li', 'strong', 'em', 'img', 'table', 'tr', 'td',
        'th', 'thead', 'tbody', 'tfoot', 'caption', 'blockquote', 'code', 'pre', 'span', 'div',
        'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
    ]

    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'table': ['border', 'cellpadding', 'cellspacing'],
        'td': ['colspan', 'rowspan', 'align', 'valign'],
        'th': ['colspan', 'rowspan', 'align', 'valign'],
        '*': ['class', 'id']
    }
