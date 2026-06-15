# import hashlib
# import os
# from werkzeug.utils import secure_filename
# from flask import current_app
# from PIL import Image
# import bleach
# import markdown

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# def compute_md5(file_data):
#     return hashlib.md5(file_data).hexdigest()

# def save_cover(file, book_id, db, Cover):
#     try:
#         file_data = file.read()
#         md5_hash = compute_md5(file_data)
        
#         existing_cover = Cover.query.filter_by(md5_hash=md5_hash).first()
#         if existing_cover:
#             existing_cover.book_id = book_id
#             db.session.commit()
#             return existing_cover
        
#         original_filename = secure_filename(file.filename)
#         extension = original_filename.rsplit('.', 1)[1].lower()
#         new_filename = f"{book_id}_{md5_hash[:8]}.{extension}"
#         filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
#         img = Image.open(file)
#         img.thumbnail((500, 700), Image.Resampling.LANCZOS)
#         img.save(filepath, optimize=True)
        
#         cover = Cover(
#             filename=new_filename,
#             mime_type=file.mimetype,
#             md5_hash=md5_hash,
#             book_id=book_id
#         )
#         db.session.add(cover)
#         return cover
#     except Exception as e:
#         print(f"Error saving cover: {e}")
#         import traceback
#         traceback.print_exc()
#         raise e

# def sanitize_html(text):
#     allowed_tags = [
#         'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
#         'ul', 'ol', 'li', 'a', 'code', 'pre', 'blockquote', 'img'
#     ]
#     allowed_attributes = {
#         'a': ['href', 'title'],
#         'img': ['src', 'alt', 'title']
#     }
#     return bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes, strip=True)

# def markdown_to_html(text):
#     md = markdown.Markdown(extensions=['extra', 'codehilite'])
#     html = md.convert(text)
#     return sanitize_html(html)

# def delete_cover_file(cover):
#     if cover:
#         filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], cover.filename)
#         if os.path.exists(filepath):
#             os.remove(filepath)


import hashlib
import os
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image
import bleach
import markdown

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def compute_md5(file_data):
    return hashlib.md5(file_data).hexdigest()

# def save_cover(file, book_id, db, Cover):
#     """Сохраняет обложку в файловую систему и создаёт запись в БД"""
#     try:
#         print(f"=== SAVING COVER START ===")
#         print(f"Book ID: {book_id}")
#         print(f"File: {file.filename if file else 'No file'}")
        
#         if not file:
#             print("No file provided")
#             return None
        
#         file_data = file.read()
#         print(f"File size: {len(file_data)} bytes")
        
#         md5_hash = compute_md5(file_data)
#         print(f"MD5 hash: {md5_hash}")
        
#         # Check if image with same hash exists
#         existing_cover = Cover.query.filter_by(md5_hash=md5_hash).first()
#         if existing_cover:
#             print(f"Cover already exists with ID: {existing_cover.id}")
#             existing_cover.book_id = book_id
#             db.session.commit()
#             return existing_cover
        
#         # Secure filename and save
#         original_filename = secure_filename(file.filename)
#         extension = original_filename.rsplit('.', 1)[1].lower()
#         new_filename = f"{book_id}_{md5_hash[:8]}.{extension}"
        
#         # Get upload folder path
#         upload_folder = current_app.config['UPLOAD_FOLDER']
#         print(f"Upload folder: {upload_folder}")
        
#         # Ensure directory exists
#         os.makedirs(upload_folder, exist_ok=True)
        
#         filepath = os.path.join(upload_folder, new_filename)
#         print(f"File will be saved to: {filepath}")
        
#         # Optimize image
#         file.seek(0)  # Reset file pointer
#         img = Image.open(file)
#         print(f"Original image size: {img.size}")
#         img.thumbnail((500, 700), Image.Resampling.LANCZOS)
#         img.save(filepath, optimize=True, quality=85)
#         print(f"Image saved, new size: {img.size}")
        
#         # Create cover record
#         cover = Cover(
#             filename=new_filename,
#             mime_type=file.mimetype,
#             md5_hash=md5_hash,
#             book_id=book_id
#         )
#         db.session.add(cover)
        
#         print("=== SAVING COVER SUCCESS ===")
#         return cover
        
#     except Exception as e:
#         print(f"Error saving cover: {e}")
#         import traceback
#         traceback.print_exc()
#         raise e
#     finally:
#         print("=== SAVING COVER END ===")

def save_cover(file, book_id, db, Cover):
    """Сохраняет обложку в файловую систему и создаёт запись в БД"""
    try:
        print(f"=== SAVING COVER START ===")
        print(f"Book ID: {book_id}")
        
        if not file or not file.filename:
            print("No file provided")
            return None
        
        file_data = file.read()
        print(f"File size: {len(file_data)} bytes")
        
        md5_hash = compute_md5(file_data)
        print(f"MD5 hash: {md5_hash}")
        
        # Check if image with same hash exists
        existing_cover = Cover.query.filter_by(md5_hash=md5_hash).first()
        if existing_cover:
            print(f"Cover already exists with ID: {existing_cover.id}")
            existing_cover.book_id = book_id
            db.session.commit()
            return existing_cover
        
        # Secure filename
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        new_filename = f"{book_id}_{md5_hash[:8]}.{extension}"
        
        # Get upload folder path
        upload_folder = current_app.config['UPLOAD_FOLDER']
        print(f"Upload folder: {upload_folder}")
        
        # Ensure directory exists
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, new_filename)
        print(f"File will be saved to: {filepath}")
        
        # Optimize image
        img = Image.open(file)
        print(f"Original image size: {img.size}")
        img.thumbnail((500, 700), Image.Resampling.LANCZOS)
        img.save(filepath, optimize=True, quality=85)
        print(f"Image saved successfully")
        
        # Create cover record - сохраняем путь относительно корня
        cover = Cover(
            filename=new_filename,
            mime_type=file.mimetype,
            md5_hash=md5_hash,
            book_id=book_id
        )
        db.session.add(cover)
        db.session.commit()
        
        print("=== SAVING COVER SUCCESS ===")
        return cover
        
    except Exception as e:
        print(f"Error saving cover: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        raise e

def sanitize_html(text):
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'a', 'code', 'pre', 'blockquote', 'img'
    ]
    allowed_attributes = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title']
    }
    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes, strip=True)

def markdown_to_html(text):
    md = markdown.Markdown(extensions=['extra', 'codehilite'])
    html = md.convert(text)
    return sanitize_html(html)

def delete_cover_file(cover):
    if cover:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], cover.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted cover file: {filepath}")