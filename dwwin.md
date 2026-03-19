# Project Context: Minimalist Flask Blog

This document serves as the core reference for the architecture, tech stack, and strict development guidelines for the Minimalist Flask Blog project. Any AI or developer working on this project must read and adhere to these specifications.

---

## 1. Technology Stack
* **Backend:** Python 3.x with Flask.
* **Database:** SQLite managed via Flask-SQLAlchemy.
* **Frontend:** HTML5, Jinja2 templating, Bootstrap 5 (via CDN).
* **Design Theme:** Strict Minimalist / Monochrome (Black, White, and Gray ONLY). No default Bootstrap colors (primary, success, danger, etc.) are allowed.

---

## 2. Directory Structure
```text
app/
│
├── app.py                  # Main Flask application, routes, and DB models
├── instance/               
│   └── blog.db             # SQLite database file (auto-generated)
├── project.md      # This documentation file
└── templates/              # Jinja2 HTML templates
    ├── base.html           # Master layout containing CSS, Bootstrap CDN, and Navbar
    ├── create.html         # Form to add a new post
    ├── dashboard.html      # Admin table view of all posts
    ├── index.html          # Public home page listing posts
    └── post.html           # Single post view

## 3. Database Schema (Models)
Table: Post
Column Name	Data Type	Constraints	Description
id	Integer	Primary Key	Unique identifier for the post.
title	String(150)	Not Null	The title of the blog post.
content	Text	Not Null	The main body/content of the post.
date_posted	DateTime	Not Null, Default: UTC Now	Timestamp of when the post was created.

## 4. Application Routes
Route	Methods	Function Name	Description
/	GET	index()	Home page. Fetches all posts ordered by date (descending) and displays excerpts.
/post/<int:post_id>	GET	post(post_id)	Fetches a single post by ID. Uses get_or_404 to handle missing posts.
/dashboard	GET	dashboard()	Admin panel displaying all posts in a structured HTML table.
/create	GET, POST	create()	Displays the creation form (GET) and handles saving new posts to the DB (POST).


## 5. 🛑 STRICT AI INSTRUCTIONS 🛑

If you are an AI assistant helping with this project, you MUST strictly obey the following rules:

    Do NOT Delete Working Code: Never remove existing, functional logic or CSS unless explicitly instructed by the user to do so.

    No Unauthorized External Libraries: Do not install or import any new Python packages, frontend libraries, fonts, or frameworks without asking for explicit permission first.

    Output ONLY Modified Code: Do NOT output the entire app.py or HTML file if you are only changing a few lines. Provide ONLY the specific function, block, or snippet that needs to be updated, and clearly indicate where it should be placed.

    Maintain the Monochrome Theme: If generating new UI components, strictly adhere to the Black, White, and Gray color palette. Do not use semantic colors like blue, green, or red.


بهذا الملف، سيكون أي نموذج ذكاء اصطناعي تستخدمه مستقبلاً ملزماً بفهم هيكل مشروعك واحترام قوانينك الصارمة.

هل ترغب في أن أساعدك الآن في كتابة ملف `requirements.txt` لتسهيل تثبيت الحزم، أم تفضل الانتقال إلى إعداد البيئة الافتراضية
