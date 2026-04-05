from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # استدعاء جديد

db = SQLAlchemy()
login_manager = LoginManager() # كائن جديد
login_manager.login_view = 'auth.login' # توجيه غير المسجلين لصفحة الدخول

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dev-secret-key' # مفتاح أمان ضروري لجلسات تسجيل الدخول
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app) # تفعيل مدير تسجيل الدخول
    
    # دالة لتحميل المستخدم الحالي
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # --- تسجيل مسارات البلوبرنت (Blueprints) ---
    from app.routes.main import main_bp
    from app.routes.posts import posts_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp # استدعاء جديد
    
    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin') # من الأفضل إضافة مسار أساسي للوحة التحكم
    app.register_blueprint(auth_bp, url_prefix='/auth') # تسجيل مسار المصادقة

    @app.context_processor
    def inject_settings():
        from app.models import SiteSetting
        settings = SiteSetting.query.first()
        return dict(site_settings=settings)
        
    return app