import os
from dotenv import load_dotenv

class Config:
    load_dotenv() 

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_ADDRESS = os.environ.get("EMAIL")
    MAIL_PASSWORD = os.environ.get("PASSWORD")
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
    RESEND_SENDER = os.environ.get("RESEND_SENDER")
    RESEND_RECEIVER = os.environ.get("RESEND_RECEIVER")

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
