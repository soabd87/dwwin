from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("⚙️ جاري تحديث قاعدة البيانات...")
    # حذف جدول الإعدادات القديم لارتباطه بعمود الإيميل
    db.session.execute(text('DROP TABLE IF EXISTS site_setting'))
    # إعادة إنشاء الجداول المفقودة (سيتم إنشاء جدول الإعدادات الجديد)
    db.create_all()
    db.session.commit()
    print("✅ تم تحديث قاعدة البيانات وإزالة حقل الإيميل بنجاح!")