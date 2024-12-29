# 🌟 Blobby - Your Personalized Blogging Platform! 📝

Welcome to **Blobby** – a beautifully crafted blogging platform where your **mind**, **expression**, and **life** take center stage! 🚀 Whether you're a writer, thinker, or storyteller, Blobby empowers you to share your thoughts with the world in style. 🌍✨

---

## 🎯 Features That Shine Bright 🌟

- 🖋️ **Rich Text Editing**: Create and edit posts effortlessly with CKEditor.
- 🖼️ **Stunning Visuals**: Add eye-catching images to your posts with ease.
- 💬 **Engage With Comments**: Let readers share their thoughts on your posts.
- 🔒 **Secure User Authentication**: Login and registration made safe and simple.
- 🎨 **Responsive Design**: Beautifully designed with Bootstrap for all devices.

---

## 🛠️ Getting Started

Follow these steps to set up and run Blobby on your local machine:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Blobby.git
cd Blobby
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file in the root directory and add the following:

```plaintext
EMAIL=your-email@example.com
PASSWORD=your-email-password
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=your-database-uri
```

### 4️⃣ Run the Application

```bash
python main.py
```

Access the app at `http://127.0.0.1:5000/`.

---

## 📂 Project Structure

```plaintext
Blobby/
├── app/                      # Main application folder
│   ├── __init__.py           # Initializes the app package
│   ├── forms.py              # Contains all forms
│   ├── models.py             # Defines database models
│   ├── routes.py             # Contains the routes (views) for the application
├── static/                   # Static files
│   ├── assets/               # Additional assets
│   ├── css/                  # CSS files
│   ├── js/                   # Javascript files
├── templates/                # Jinja2 templates for rendering HTML pages
│   ├── about.html            # About page
│   ├── contact.html          # Contact page
│   ├── footer.html           # Footer template
│   ├── header.html           # Header template
│   ├── index.html            # Homepage displaying all posts
│   ├── login.html            # Login page
│   ├── make-post.html        # Page for creating or editing posts
│   ├── post.html             # Page for viewing individual posts
│   └── register.html         # User registration page
├── .gitignore                # Git ignore file
├── config.py                 # Configuration file
├── requirements.txt          # Python dependencies for the project
├── run.py                    # Entry point to run the Flask app
├── vercel.json               # Vercel configuration for deployment
└── README.md                 # Project documentation
```

---

## 🛠️ Tech Stack

Blobby is built with the following awesome technologies:

- **Backend**: [Flask](https://flask.palletsprojects.com/) 🐍  
- **Frontend**: [Bootstrap](https://getbootstrap.com/) 🎨  
- **Rich Text Editor**: [CKEditor](https://ckeditor.com/) 🖋️  
- **Database**: [PostgreSQL](https://www.postgresql.org/) (hosted on [Vercel](https://vercel.com/)) 🗃️  
- **Deployment**: [Vercel](https://vercel.com/) 🚀  

---

## ❤️ Contribute

We love contributions! 🛠️ Found a bug? Have a cool feature idea? Feel free to open an issue or submit a pull request. Together, we can make Blobby even better! 💪

---

## 🙌 Connect With Me

Let's get social! Connect with me on:

- 🐦 [Twitter](https://twitter.com/SAMEETPATIL5)
- 📸 [Instagram](https://www.instagram.com/sameetpatil_5/)
- 💼 [LinkedIn](https://www.linkedin.com/in/sameetpatil5/)
- 💻 [GitHub](https://github.com/sameetpatil5)

---

✨ **Blobby**: Your blog, your story, your world. 🌍💖

---

Thanks to [Najmun Nahar](https://www.flaticon.com/authors/najmunnahar) for the Logo for the Blobby Website.
