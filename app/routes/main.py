from flask import Blueprint, render_template
from app.models import Post

# إنشاء البلوبرنت الخاص بالمسارات الرئيسية
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """الصفحة الرئيسية: تعرض جميع المقالات مرتبة من الأحدث للأقدم"""
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    # سنحافظ على اسم القالب القديم مؤقتاً حتى نرتب القوالب في الخطوة القادمة
    return render_template('index.html', posts=posts)