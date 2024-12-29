# forms.py - This file contains various WTForms used in the application.

from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    StringField,
    SubmitField,
    PasswordField,
    TextAreaField,
    URLField,
)
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


# WTForm for creating & editing a Blog Post
class BlogPostForm(FlaskForm):
    """
    CreatePostForm is used to create a new blog post or edit an existing blog post.
    It contains the following fields:
    - title: A required string field for the blog post title.
    - subtitle: A required string field for the blog post subtitle.
    - img_url: A required URL field for the blog post image URL.
    - body: A required CKEditor field for the blog content.
    - submit: A submit field for submitting the form.
    """

    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = URLField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# WTForm to Register new users
class RegisterForm(FlaskForm):
    """
    RegisterForm is used for registering new users.
    It contains the following fields:
    - email: A required email field for the user's email address.
    - password: A required password field for the user's password.
    - name: A required string field for the user's name.
    - submit: A submit field for submitting the form.
    """

    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    username = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Register")


# WTForm to Login existing users
class LoginForm(FlaskForm):
    """
    LoginForm is used for users to log in.
    It contains the following fields:
    - email: A required email field for the user's email address.
    - password: A required password field for the user's password.
    - submit: A submit field for submitting the form.
    """

    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


# WTForm to add comments under Blog Post
class CommentForm(FlaskForm):
    """
    CommentForm is used for users to add comments under a blog post.
    It contains the following fields:
    - comment_text: A required TextArea field for the user's comment.
    - submit: A submit field for submitting the form.
    """

    comment_text = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


# WTForm to contact the Admin
class ContactFrom(FlaskForm):
    """
    ContactForm is used for users to contact the admin.
    It contains the following fields:
    - name: A required string field for the user's name
    - email: A required email field for the user's email address.
    - message: A required string field for the user's message.
    - submit: A submit field for submitting the form.
    """

    username = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
