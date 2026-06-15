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
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    @app.context_processor
    def utility_processor():
        def get_args_without_page(args):
            """Удаляет параметр page из request.args и возвращает словарь"""
            args_dict = args.to_dict()
            args_dict.pop('page', None)
            return args_dict
        
        return dict(get_args_without_page=get_args_without_page)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    from app.blueprints.auth import auth_bp
    from app.blueprints.books import books_bp
    from app.blueprints.reviews import reviews_bp
    from app.blueprints.main import main_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(main_bp)
    
    return app