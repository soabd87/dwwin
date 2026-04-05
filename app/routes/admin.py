from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user # أضف current_user هنا
from app import db
from app.models import Post, SiteSetting, Category # تمت إضافة Category
from app.utils import process_and_save_image
from werkzeug.security import generate_password_hash # أضف هذا السطر

# إنشاء البلوبرنت الخاص بلوحة التحكم
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required # <--- أضف هذا السطر
def dashboard():
    """لوحة التحكم: تعرض جدولاً بجميع المقالات لإدارتها"""
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)

@admin_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """صفحة إضافة مقال جديد"""
    categories = Category.query.all() # جلب جميع الأقسام لعرضها في القائمة المنسدلة
    
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        category_id = request.form.get('category_id') # جلب رقم القسم المختار

        image_file = request.files.get('image')
        image_filename = process_and_save_image(image_file)
        
        new_post = Post(title=post_title, content=post_content, category_id=category_id, image_filename=image_filename)
        
        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            return f"حدث خطأ أثناء إضافة المقال: {e}"
            
    return render_template('admin/create.html', categories=categories)

@admin_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """تعديل مقال موجود"""
    post = Post.query.get_or_404(post_id)
    categories = Category.query.all() # جلب الأقسام
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category_id = request.form.get('category_id') # تحديث القسم

        # --- السطور الجديدة لتحديث الصورة إن وُجدت ---
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            new_image_name = process_and_save_image(image_file)
            if new_image_name:
                post.image_filename = new_image_name
        try:
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            return f"حدث خطأ أثناء تعديل المقال: {e}"
            
    return render_template('admin/edit.html', post=post, categories=categories)

@admin_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required # <--- أضف هذا السطر
def delete_post(post_id):
    """حذف مقال"""
    post = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        return f"حدث خطأ أثناء حذف المقال: {e}"
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """صفحة إعدادات الموقع وتعديل بيانات المدير"""
    # جلب الإعدادات أو إنشاء صف جديد إذا لم يكن موجوداً
    site_settings = SiteSetting.query.first()
    if not site_settings:
        site_settings = SiteSetting(site_name="Minimalist Blog")
        db.session.add(site_settings)
        db.session.commit()

    if request.method == 'POST':
        # تحديث اسم الموقع
        site_settings.site_name = request.form['site_name']
        
        # تحديث بيانات المدير
        current_user.username = request.form['username']
        
        # التحقق مما إذا كان قد أدخل كلمة مرور جديدة
        new_password = request.form.get('new_password')
        if new_password and new_password.strip() != '':
            current_user.password_hash = generate_password_hash(new_password)
            
        try:
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            return f"حدث خطأ أثناء حفظ التعديلات: {e}"

    return render_template('admin/settings.html', settings=site_settings)

@admin_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    """صفحة إدارة الأقسام (إضافة وعرض)"""
    if request.method == 'POST':
        category_name = request.form.get('name')
        if category_name:
            new_category = Category(name=category_name)
            try:
                db.session.add(new_category)
                db.session.commit()
            except Exception as e:
                return f"حدث خطأ أثناء إضافة القسم (قد يكون الاسم موجوداً مسبقاً): {e}"
        return redirect(url_for('admin.manage_categories'))

    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)