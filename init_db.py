from app import create_app, db
from app.models import User, Role, Genre
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    
    db.create_all()
    
    roles = [
        Role(name='admin', description='Полный доступ к системе'),
        Role(name='moderator', description='Может редактировать книги и модерировать рецензии'),
        Role(name='user', description='Может оставлять рецензии')
    ]
    
    for role in roles:
        db.session.add(role)
    
    db.session.commit()
    
    admin = User(
        login='admin',
        password_hash=generate_password_hash('admin123'),
        last_name='Администратор',
        first_name='Системный',
        patronymic='Администратор',
        role_id=1
    )
    
    db.session.add(admin)
    
    moderator = User(
        login='moderator',
        password_hash=generate_password_hash('moder123'),
        last_name='Модератор',
        first_name='Модератор',
        patronymic='Модератор',
        role_id=2
    )
    
    db.session.add(moderator)
    
    user = User(
        login='user',
        password_hash=generate_password_hash('user123'),
        last_name='Пользователь',
        first_name='Обычный',
        patronymic='Пользователь',
        role_id=3
    )
    
    db.session.add(user)
    
    genres = [
        Genre(name='Фантастика'),
        Genre(name='Детектив'),
        Genre(name='Роман'),
        Genre(name='Научная литература'),
        Genre(name='Поэзия'),
        Genre(name='Приключения'),
        Genre(name='Триллер'),
        Genre(name='Историческая проза')
    ]
    
    for genre in genres:
        db.session.add(genre)
    
    db.session.commit()
    
    print("Database initialized successfully!")
    print("Default users created:")
    print("Admin: login='admin', password='admin123'")
    print("Moderator: login='moderator', password='moder123'")
    print("User: login='user', password='user123'")