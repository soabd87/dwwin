from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# تهيئة تطبيق Flask
app = Flask(__name__)

# إعدادات قاعدة البيانات (SQLite)
# سيتم إنشاء ملف blog.db في مجلد instance (تلقائياً في الإصدارات الحديثة)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # إيقاف هذه الخاصية لتوفير الموارد

# ربط قاعدة البيانات بالتطبيق
db = SQLAlchemy(app)

# ---------------------------------------------------------
# نموذج قاعدة البيانات (Database Model)
# ---------------------------------------------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # نستخدم timezone.utc لضمان توحيد التوقيت بغض النظر عن الخادم
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Post '{self.title}'>"

# ---------------------------------------------------------
# مسارات التطبيق (Routes)
# ---------------------------------------------------------

@app.route('/')
def index():
    """الصفحة الرئيسية: تعرض جميع المقالات مرتبة من الأحدث للأقدم"""
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    """صفحة المقال الفردي: تعرض محتوى المقال بناءً على المعرف (ID)"""
    # get_or_404 تقوم بإرجاع خطأ 404 تلقائياً إذا لم يكن المقال موجوداً
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/dashboard')
def dashboard():
    """لوحة التحكم: تعرض جدولاً بجميع المقالات لإدارتها"""
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('dashboard.html', posts=posts)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """صفحة إضافة مقال جديد: تعالج عرض النموذج (GET) وحفظ البيانات (POST)"""
    if request.method == 'POST':
        # جلب البيانات من النموذج
        post_title = request.form['title']
        post_content = request.form['content']
        
        # إنشاء كائن مقال جديد
        new_post = Post(title=post_title, content=post_content)
        
        try:
            # إضافة المقال إلى قاعدة البيانات وحفظ التغييرات
            db.session.add(new_post)
            db.session.commit()
            # إعادة التوجيه إلى لوحة التحكم بعد النجاح
            return redirect(url_for('dashboard'))
        except Exception as e:
            return f"حدث خطأ أثناء إضافة المقال: {e}"
            
    # في حالة الطلب GET، يتم عرض صفحة النموذج
    return render_template('create.html')

# ---------------------------------------------------------
# تشغيل التطبيق
# ---------------------------------------------------------
if __name__ == "__main__":
    # إنشاء جداول قاعدة البيانات إذا لم تكن موجودة
    # الطريقة الحديثة تتطلب استخدام app_context
    with app.app_context():
        db.create_all()
        
    # تشغيل خادم التطوير (ضع debug=False عند النشر الفعلي)
    app.run(debug=True)
