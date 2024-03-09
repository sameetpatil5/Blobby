import os
from dotenv import load_dotenv
from datetime import date
from flask import (
    Flask,
    abort,
    render_template,
    redirect,
    session,
    url_for,
    flash,
    request,
)
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import (
    UserMixin,
    login_required,
    login_user,
    LoginManager,
    current_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import BlogPostForm, RegisterForm, LoginForm, CommentForm, ContactFrom
import smtplib

# Load environment variables
load_dotenv()

# Load email credentials from environment variables
MAIL_ADDRESS = os.environ.get("EMAIL")
MAIL_APP_PW = os.environ.get("PASSWORD")

# Initialize Flask app
app = Flask(__name__)
# Load secret key from environment variables
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# Initialize CKEditor
ckeditor = CKEditor(app)
# Initialize Bootstrap
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize Gravatar
gravatar = Gravatar(
    app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)


# Create database instance
class Base(DeclarativeBase):
    pass


# Configure database URI from environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Define User model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


# Define BlogPost model
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")


# Define Comment model
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text: Mapped[str] = mapped_column(Text, nullable=False)


# Create all tables
with app.app_context():
    db.create_all()


# Load user into Login
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Define context processor for template rendering
@app.context_processor
def context_processor():
    return dict(
        logged_in=session.get("logged_in", False),
        is_admin=session.get("is_admin", False),
        # user_email=session.get("user_email", None),
        current_user=current_user,
    )


# Define admin-only decorator
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("is_admin"):
            return func(*args, **kwargs)
        else:
            return abort(403)

    return wrapper


# Check if user is admin
def is_admin(current_user):
    if current_user.id == 1:
        return True
    else:
        return False


# Register new users
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if db.session.execute(
            db.select(User).where(User.email == register_form.email.data)
        ).scalar():
            session["user_email"] = register_form.email.data
            flash("This user already exists, Please login instead")
            return redirect(url_for("login"))
        else:
            new_user = User(
                username=register_form.username.data,
                email=register_form.email.data,
                password=generate_password_hash(
                    password=register_form.password.data,
                    method="pbkdf2:sha512",
                    salt_length=8,
                ),
            )
            db.session.add(new_user)
            db.session.commit()
            user = load_user(new_user.id)
            login_user(user)
            session["logged_in"] = True
            return redirect(url_for("get_all_posts"))
    return render_template(
        "register.html", form=register_form, current_user=current_user
    )


# User login
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if session.get("user_email") is not None:
        login_form.email.data = session.get("user_email")
    if login_form.validate_on_submit():
        user_login = db.session.execute(
            db.select(User).where(User.email == login_form.email.data)
        ).scalar()
        if not user_login:
            flash("Please enter a valid email id.")
            return redirect(url_for("login"))
        elif not check_password_hash(
            pwhash=user_login.password, password=login_form.password.data
        ):
            flash("Please enter the correct password")
            return redirect(url_for("login"))
        else:
            user = load_user(user_login.id)
            if is_admin(user):
                session["is_admin"] = True
            login_user(user)
            session["logged_in"] = True
            return redirect(url_for("get_all_posts"))
    return render_template("login.html", form=login_form, current_user=current_user)


# User logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session["is_admin"] = False
    session["logged_in"] = False
    session["user_email"] = None
    return redirect(url_for("get_all_posts"))


# Display all posts
@app.route("/")
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


# Show individual post
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm(comment_text=" ")
    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                text=comment_form.comment_text.data,
                comment_author=current_user,
                parent_post=requested_post,
            )
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
    return render_template(
        "post.html", post=requested_post, form=comment_form, current_user=current_user
    )


# Add new post (admin only)
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    createpost_form = BlogPostForm()
    if createpost_form.validate_on_submit():
        new_post = BlogPost(
            title=createpost_form.title.data,
            subtitle=createpost_form.subtitle.data,
            body=createpost_form.body.data,
            img_url=createpost_form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template(
        "make-post.html", form=createpost_form, current_user=current_user
    )


# Edit post (admin only)
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = BlogPostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template(
        "make-post.html", form=edit_form, is_edit=True, current_user=current_user
    )


# Delete post (admin only)
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


# About page
@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        MESSAGE = f"Subject: {request.form['username']} has sent a messsage!!!\n\n \
                    Name: {request.form['username']}\n \
                    E-mail: {request.form['email']}\n \
                    Phone No.: {request.form['phone']}\n \
                    Message: {request.form['message']}"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MAIL_ADDRESS, password=MAIL_APP_PW)
            connection.sendmail(
                from_addr=MAIL_ADDRESS, to_addrs=MAIL_ADDRESS, msg=MESSAGE
            )
            connection.close()
        return render_template("contact.html", msg_sent=True)
    else:
        if current_user.is_authenticated:
            name = current_user.username
            email = current_user.email
        else:
            name = ""
            email = ""
        return render_template(
            "contact.html",
            msg_sent=False,
            name=name,
            email=email,
            current_user=current_user,
        )


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
