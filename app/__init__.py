# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, current_user
# from config import Config
# import os

# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Для выполнения данного действия необходимо пройти процедуру аутентификации'

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
    
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
#     db.init_app(app)
#     login_manager.init_app(app)
    
#     @app.context_processor
#     def utility_processor():
#         def get_args_without_page(args):
#             args_dict = args.to_dict()
#             args_dict.pop('page', None)
#             return args_dict
        
#         return dict(get_args_without_page=get_args_without_page)
    
#     @login_manager.user_loader
#     def load_user(user_id):
#         from app.models import User
#         return User.query.get(int(user_id))
    
#     from app.blueprints.auth import auth_bp
#     from app.blueprints.books import books_bp
#     from app.blueprints.reviews import reviews_bp
#     from app.blueprints.main import main_bp
    
#     app.register_blueprint(auth_bp, url_prefix='/auth')
#     app.register_blueprint(books_bp, url_prefix='/books')
#     app.register_blueprint(reviews_bp, url_prefix='/reviews')
#     app.register_blueprint(main_bp)
    
#     return app

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Для выполнения данного действия необходимо пройти процедуру аутентификации'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Создаём папку для загрузок
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    print(f"Upload folder: {upload_folder}")
    print(f"Upload folder exists: {os.path.exists(upload_folder)}")
    
    # Также создаём папку в static для обратной совместимости
    static_uploads = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(static_uploads, exist_ok=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    @app.context_processor
    def utility_processor():
        def get_args_without_page(args):
            args_dict = args.to_dict()
            args_dict.pop('page', None)
            return args_dict
        return dict(get_args_without_page=get_args_without_page)
    
    # @login_manager.user_loader
    # def load_user(user_id):
    #     from app.models import User
    #     return User.query.get(int(user_id))
    
    # # Настройка для раздачи файлов из папки covers
    # @app.route('/covers/<path:filename>')
    # def serve_cover(filename):
    #     from flask import send_from_directory
    #     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # from app.blueprints.auth import auth_bp
    # from app.blueprints.books import books_bp
    # from app.blueprints.reviews import reviews_bp
    # from app.blueprints.main import main_bp
    
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(books_bp, url_prefix='/books')
    # app.register_blueprint(reviews_bp, url_prefix='/reviews')
    # app.register_blueprint(main_bp)
    
    # return app

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # Маршрут для раздачи файлов обложек из Volume
    @app.route('/covers/<path:filename>')
    def serve_cover(filename):
        from flask import send_from_directory, abort
        import os
        try:
            # Проверяем, что файл существует в папке UPLOAD_FOLDER
            upload_folder = app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, filename)
            if not os.path.exists(file_path):
                # Логируем ошибку
                print(f"File not found: {file_path}")
                abort(404)
            return send_from_directory(upload_folder, filename)
        except Exception as e:
            print(f"Error serving cover: {e}")
            abort(404)

    from app.blueprints.auth import auth_bp
    from app.blueprints.books import books_bp
    from app.blueprints.reviews import reviews_bp
    from app.blueprints.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(main_bp)

    return app