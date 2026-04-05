import os
from app import create_app, db
from werkzeug.security import generate_password_hash # إضافة مكتبة تشفير كلمة المرور

# إنشاء نسخة من التطبيق
app = create_app()

def check_and_create_db(app):
    """دالة للتحقق من وجود قاعدة البيانات وإنشائها وإضافة مدير افتراضي إذا لم تكن موجودة"""
    # تحديد مسار قاعدة البيانات داخل مجلد instance
    db_path = os.path.join(app.instance_path, 'blog.db')
    
    # إذا لم يكن الملف موجوداً، قم بإنشائه
    if not os.path.exists(db_path):
        print("⚙️ قاعدة البيانات غير موجودة. جاري إنشاؤها تلقائياً...")
        with app.app_context():
            from app import models  # استدعاء الجداول ليتعرف عليها فلاسك
            from app.models import User # استدعاء نموذج المستخدم
            
            # التأكد من وجود مجلد instance
            os.makedirs(app.instance_path, exist_ok=True)
            db.create_all()
            print("✅ تم إنشاء قاعدة البيانات (blog.db) بنجاح!")
            
            # إنشاء حساب المدير الافتراضي
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                hashed_password = generate_password_hash('123456789')
                new_admin = User(username='admin', password_hash=hashed_password)
                db.session.add(new_admin)
                db.session.commit()
                print("✅ تم إنشاء حساب المدير الافتراضي بنجاح (المستخدم: admin | المرور: 123456789)")

if __name__ == "__main__":
    # تشغيل فحص قاعدة البيانات قبل إقلاع السيرفر
    check_and_create_db(app)
    
    # تشغيل خادم التطوير
    app.run(debug=True, port=5200)