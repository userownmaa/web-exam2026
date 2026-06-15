# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key-here-346381'
    
#     database_url = os.environ.get('DATABASE_URL')
    
#     if database_url:
#         SQLALCHEMY_DATABASE_URI = database_url.replace('postgres://', 'postgresql://', 1)
#     else:
#         DB_USER = os.environ.get('DB_USER', 'library_user')
#         DB_PASSWORD = os.environ.get('DB_PASSWORD', 'web-exam2026')
#         DB_HOST = os.environ.get('DB_HOST', 'localhost')
#         DB_PORT = os.environ.get('DB_PORT', '5432')
#         DB_NAME = os.environ.get('DB_NAME', 'library_db')
#         SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
#     BOOKS_PER_PAGE = 6

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key-here-346381'
    
    # Database
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url.replace('postgres://', 'postgresql://', 1)
    else:
        DB_USER = os.environ.get('DB_USER', 'library_user')
        DB_PASSWORD = os.environ.get('DB_PASSWORD', 'web-exam2026')
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_PORT = os.environ.get('DB_PORT', '5432')
        DB_NAME = os.environ.get('DB_NAME', 'library_db')
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings — используем Railway Volume, если он есть
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Проверяем, есть ли переменная от Railway Volume
    if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'):
        # Используем путь из Railway Volume
        UPLOAD_FOLDER = os.path.join(os.environ['RAILWAY_VOLUME_MOUNT_PATH'])
    else:
        # Локальная разработка
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    BOOKS_PER_PAGE = 6