from flask import Blueprint, render_template, redirect, url_for, flash, session, abort, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from api.models import User, BlogPost, Comment
from api.forms import BlogPostForm, RegisterForm, LoginForm, CommentForm, ContactFrom
from api import db
from flask import current_app
from functools import wraps
import smtplib
import os
import bleach
import re

# Load email credentials from environment variables
MAIL_ADDRESS = os.environ.get("EMAIL")
MAIL_APP_PW = os.environ.get("PASSWORD")

# Sanitize content from User input
def sanitize(text):
    allowed_tags = current_app.config['ALLOWED_TAGS']
    allowed_attributes = current_app.config['ALLOWED_ATTRIBUTES']
    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )

# Create a Blueprint for routes
routes_bp = Blueprint("routes", __name__)

# Admin-only decorator
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("is_admin"):
            return func(*args, **kwargs)
        else:
            return abort(403)
    return wrapper

# Context processor for template rendering
@routes_bp.app_context_processor
def context_processor():
    return dict(
        logged_in=session.get("logged_in", False),
        is_admin=session.get("is_admin", False),
        current_user=current_user,
    )

# User registration
@routes_bp.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if User.query.filter_by(email=register_form.email.data).first():
            flash("This user already exists. Please login instead.", "warning")
            return redirect(url_for("routes.login"))
        new_user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=generate_password_hash(register_form.password.data),
        )
        # db.session.add(new_user)
        # db.session.commit()
        # login_user(new_user)
        # session["logged_in"] = True
        # return redirect(url_for("routes.get_all_posts"))
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session["logged_in"] = True
            flash("Registration successful!", "success")
            return redirect(url_for("routes.get_all_posts"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
    return render_template("register.html", form=register_form)

# User login
@routes_bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user)
            session["is_admin"] = user.id == 1
            session["logged_in"] = True
            return redirect(url_for("routes.get_all_posts"))
        flash("Invalid email or password.")
    return render_template("login.html", form=login_form)

# User logout
@routes_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("routes.get_all_posts"))

# Display all posts
@routes_bp.route("/")
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)

# Show individual post
@routes_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            # text=form.comment_text.data, comment_author=current_user, parent_post=post
            text=sanitize(form.comment_text.data), comment_author=current_user, parent_post=post
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("routes.show_post", post_id=post.id))

    sanitized_post_body = sanitize(post.body)
    sanitized_comments_text = [sanitize(comment.text) for comment in post.comments]
    # print(sanitized_comments_text)
    # print([comments.text for comments in post.comments])
    comments_with_sanitized_text = zip(post.comments, sanitized_comments_text)
    return render_template("post.html", post=post, form=form, sanitized_post_body=sanitized_post_body, comments_with_sanitized_text=comments_with_sanitized_text)

# Add a new post (admin only)
@routes_bp.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=sanitize(form.body.data),
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("routes.get_all_posts"))
    return render_template("make-post.html", form=form)

# Edit a post (admin only)
@routes_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = sanitize(form.body.data)
        post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for("routes.show_post", post_id=post.id))
    return render_template("make-post.html", form=form, is_edit=True)

# Delete a post (admin only)
@routes_bp.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("routes.get_all_posts"))

# About page
@routes_bp.route("/about")
def about():
    return render_template("about.html")

# Contact page
@routes_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = f"Subject: {request.form['name']} has sent a message!!!\n\n \
                    Name: {request.form['name']}\n \
                    E-mail: {request.form['email']}\n \
                    Message: {request.form['message']}"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MAIL_ADDRESS, MAIL_APP_PW)
            connection.sendmail(MAIL_ADDRESS, MAIL_ADDRESS, message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)
