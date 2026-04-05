from flask import Blueprint, render_template
from app.models import Post, Category # تمت إضافة Category هنا

# إنشاء البلوبرنت الخاص بالمقالات
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/post/<int:post_id>')
def post(post_id):
    """صفحة المقال الفردي: تعرض محتوى المقال بناءً على المعرف"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post=post)

# ----------------- الإضافة الجديدة -----------------
@posts_bp.route('/category/<int:category_id>')
def category_posts(category_id):
    """صفحة عرض تدوينات قسم معين"""
    # جلب القسم أو إرجاع خطأ 404 إذا لم يكن موجوداً
    category = Category.query.get_or_404(category_id)
    
    # جلب التدوينات التابعة لهذا القسم فقط، مرتبة من الأحدث للأقدم
    posts = Post.query.filter_by(category_id=category.id).order_by(Post.date_posted.desc()).all()
    
    return render_template('posts/category.html', category=category, posts=posts)