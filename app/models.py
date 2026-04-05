from datetime import datetime, timezone
from flask_login import UserMixin
from app import db # استدعاء كائن قاعدة البيانات من ملف __init__.py

# أضف هذا الكلاس الجديد في أي مكان (مثلاً تحت كلاس Post)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    # العلاقة: القسم الواحد يحتوي على عدة مقالات
    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category '{self.name}'>"

# استبدل كلاس Post الحالي بهذا الكود
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    # العمود الجديد: مفتاح أجنبي يربط المقال بالقسم
    # جعلناه nullable=True مؤقتاً حتى لا تحدث مشكلة مع المقالات القديمة الموجودة في القاعدة
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Post '{self.title}'>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

  
    def __repr__(self):
        return f"<User '{self.username}'>"

class SiteSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False, default="Minimalist Blog")

    def __repr__(self):
        return f"<SiteSetting '{self.site_name}'>"
    