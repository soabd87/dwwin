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
dwwin/
│
├── .env                   # (ملف مخفي لا يظهر في أمر ls العادي، لكن تأكد من وجوده)
├── requirements.txt
├── run.py
├── update-db.py
├── dwwin.md
├── instance/
│   └── blog.db            # قاعدة البيانات تم إنشاؤها بنجاح
│
└── app/
    ├── __init__.py
    ├── models.py
    ├── utils.py
    │
    ├── routes/
    │   ├── admin.py
    │   ├── auth.py
    │   ├── comments.py
    │   ├── main.py
    │   └── posts.py
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── uploads/       # (مجلد فارغ جاهز لرفع الصور مستقبلاً)
    │
    └── templates/
        ├── base.html
        ├── index.html
        ├── admin/
        │   ├── create.html
        │   ├── categories.html
        │   ├── dashboard.html
        │   └── edit.html      # تم إضافة قالب التعديل
        ├── auth/          # (مجلد فارغ جاهز لقوالب تسجيل الدخول)
        │   └── login.html     
        └── posts/
            ├── category.html
            └── post.html

## 3. Database Schema (Models)
**Table: Post**
 * `id` (Integer, Primary Key) - Unique identifier for the post.
 * `title` (String(150), Not Null) - The title of the blog post.
 * `content` (Text, Not Null) - The main body/content of the post.
 * `date_posted` (DateTime, Not Null, Default: UTC Now) - Timestamp of when the post was created.

**Table: Category**
* `id` (Integer, Primary Key) - Unique identifier for the category.
* `name` (String(50), Unique, Not Null) - The name of the category.
* `posts` (Relationship) - One-to-Many relationship with Post.

**Table: User**
* `id` (Integer, Primary Key)
* `username` (String(50), Unique, Not Null)
* `password_hash` (String(256), Not Null)

**Table: SiteSetting**
* `id` (Integer, Primary Key)
* `site_name` (String(100), Not Null, Default: "Minimalist Blog")


## 4. Application Routes

**Auth Routes (`app/routes/auth.py`):**
* `GET, POST /auth/login` : تسجيل دخول المدير.
* `GET /auth/logout` : تسجيل الخروج (يتطلب تسجيل دخول).

**Admin Routes (`app/routes/admin.py`):**
* `GET /dashboard` : يعرض لوحة التحكم وجدول التدوينات.
* `GET, POST /create` : يعرض نموذج إضافة تدوينة جديدة ويقوم بحفظها في قاعدة البيانات.
* `GET, POST /edit_post/<int:post_id>` : يجلب بيانات تدوينة محددة، يعرضها في نموذج، ويحفظ التعديلات.
* `POST /delete_post/<int:post_id>` : يقوم بحذف تدوينة محددة من قاعدة البيانات (يتطلب POST لأسباب أمنية).
* `GET, POST /admin/settings` : تعديل إعدادات الموقع (اسم الموقع) وتعديل بيانات دخول المدير (اسم المستخدم وكلمة المرور).
* `GET, POST /categories` : صفحة إدارة الأقسام (إضافة وعرض الأقسام الحالية).
* `image_filename` (String(255), Nullable) - Stores the generated WebP thumbnail filename.

**Posts Routes (`app/routes/posts.py`):**
* `GET /post/<int:post_id>` : يعرض المقال الفردي.
* `GET /category/<int:category_id>` : يعرض جميع المقالات التابعة لقسم معين.



## 5. 🛑 STRICT AI INSTRUCTIONS 🛑**
If you are an AI assistant helping with this project, you MUST strictly obey the following rules:

1. **Do NOT Delete Working Code:** Never remove existing, functional logic or CSS unless explicitly instructed by the user to do so.
2. **No Unauthorized External Libraries:** Do not install or import any new Python packages, frontend libraries, fonts, or frameworks without asking for explicit permission first.
3. **Output ONLY Modified Code:** Do NOT output the entire app.py or HTML file if you are only changing a few lines. Provide ONLY the specific function, block, or snippet that needs to be updated, and clearly indicate where it should be placed.
4. **Maintain the Monochrome Theme:** If generating new UI components, strictly adhere to the Black, White, and Gray color palette. Do not use semantic colors like blue, green, or red.
5. **Discuss Before Coding:** Do not write any new code before discussing the idea with me and waiting for my approval.
6. **Request Files First:** Do not assume the content of any file. Ask me to provide its current content before modifying it.
7. **Continuous Context Update:** After successfully completing any feature, the context file must be updated immediately. **Do NOT output the entire context file.** Provide ONLY the specific section or lines that need to be modified. You must explicitly specify the type of modification (e.g., "Addition: [what is added]", "Deletion: [what is removed]", or "Replacement: [what is removed and what replaces it]").
8. **Safe Database Updates (NO DELETION):** NEVER instruct the user to delete the SQLite database file (`blog.db`) when modifying the schema or adding new tables. Instead, provide the update logic to be placed inside `update-db.py` (assume its current content can be safely overwritten) using safe methods like `db.create_all()`. The user will execute this script manually via `python3 update-db.py`.


