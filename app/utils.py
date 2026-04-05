import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image

def process_and_save_image(upload_file):
    """
    تستقبل ملف الصورة المرفوع، تحذف الميتا داتا (EXIF)،
    تحولها إلى WebP، وتضغطها، ثم تحفظها.
    """
    if not upload_file or upload_file.filename == '':
        return None
    
    # إنشاء اسم ملف فريد
    unique_filename = f"{uuid.uuid4().hex}.webp"
    
    # تحديد مسار الحفظ (تأكد من وجود مجلد app/static/uploads/)
    upload_folder = os.path.join('app', 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, unique_filename)

    # معالجة الصورة
    try:
        with Image.open(upload_file) as img:
            # تحويل الصورة إلى RGB للتوافق الكامل مع WebP
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # حذف الميتا داتا بإنشاء صورة جديدة ونقل البيكسلات فقط
            data = list(img.getdata())
            image_without_exif = Image.new(img.mode, img.size)
            image_without_exif.putdata(data)
            
            # حفظ كـ WebP مع ضغط بنسبة 80%
            image_without_exif.save(save_path, format='WEBP', quality=80)
            
        return unique_filename
    except Exception as e:
        print(f"خطأ في معالجة الصورة: {e}")
        return None