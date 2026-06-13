# from flask import Blueprint, render_template, request, url_for
# from flask_login import current_user
# from app.models import Book, Genre, Review
# from app.forms import SearchForm
# from sqlalchemy import or_, and_
# from config import Config

# main_bp = Blueprint('main', __name__)

# @main_bp.route('/', methods=['GET', 'POST'])
# def index():
#     # Initialize search form
#     form = SearchForm()
    
#     # Get all genres and years for search filters
#     all_genres = Genre.query.order_by('name').all()
#     all_years = sorted(set([b.year for b in Book.query.all()]), reverse=True)
    
#     form.genre.choices = [(g.id, g.name) for g in all_genres]
#     form.year.choices = [(y, str(y)) for y in all_years]
    
#     # Base query
#     query = Book.query
    
#     # Search filter - поддержка GET параметров для пагинации
#     search_active = False
    
#     # Проверяем как POST (отправка формы) так и GET (параметры из URL)
#     if request.method == 'POST':
#         # Сохраняем параметры поиска в сессию или перенаправляем с GET параметрами
#         args = {}
#         if form.title.data:
#             args['title'] = form.title.data
#         if form.author.data:
#             args['author'] = form.author.data
#         if form.genre.data:
#             args['genre'] = ','.join(str(g) for g in form.genre.data)
#         if form.year.data:
#             args['year'] = ','.join(str(y) for y in form.year.data)
#         if form.pages_from.data:
#             args['pages_from'] = form.pages_from.data
#         if form.pages_to.data:
#             args['pages_to'] = form.pages_to.data
        
#         if args:
#             return redirect(url_for('main.index', **args))
    
#     # Получаем параметры из GET запроса
#     title = request.args.get('title', '')
#     author = request.args.get('author', '')
#     genre_ids = request.args.get('genre', '')
#     year_values = request.args.get('year', '')
#     pages_from = request.args.get('pages_from', '', type=int)
#     pages_to = request.args.get('pages_to', '', type=int)
    
#     if title or author or genre_ids or year_values or pages_from or pages_to:
#         search_active = True
#         # Заполняем форму для отображения
#         form.title.data = title
#         form.author.data = author
        
#         if title:
#             query = query.filter(Book.title.ilike(f'%{title}%'))
#         if author:
#             query = query.filter(Book.author.ilike(f'%{author}%'))
#         if genre_ids:
#             genre_list = [int(g) for g in genre_ids.split(',') if g]
#             if genre_list:
#                 query = query.filter(Book.genres.any(Genre.id.in_(genre_list)))
#             form.genre.data = genre_list
#         if year_values:
#             year_list = [int(y) for y in year_values.split(',') if y]
#             if year_list:
#                 query = query.filter(Book.year.in_(year_list))
#             form.year.data = year_list
#         if pages_from:
#             query = query.filter(Book.pages >= pages_from)
#         if pages_to:
#             query = query.filter(Book.pages <= pages_to)
    
#     # Order by newest first
#     query = query.order_by(Book.year.desc(), Book.created_at.desc())
    
#     # Pagination
#     page = request.args.get('page', 1, type=int)
#     pagination = query.paginate(page=page, per_page=Config.BOOKS_PER_PAGE, error_out=False)
#     books = pagination.items
    
#     return render_template('index.html', 
#                          books=books, 
#                          pagination=pagination, 
#                          form=form, 
#                          search_active=search_active,
#                          genres=all_genres,
#                          years=all_years)

from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from app.models import Book, Genre, Review
from sqlalchemy import or_, and_
from config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    # Base query
    query = Book.query
    
    # Get filter parameters from GET request
    title = request.args.get('title', '').strip()
    author = request.args.get('author', '').strip()
    genre_ids = request.args.get('genre', '')
    year_values = request.args.get('year', '')
    pages_from = request.args.get('pages_from', '', type=int)
    pages_to = request.args.get('pages_to', '', type=int)
    
    # Apply filters
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if genre_ids:
        genre_list = [int(g) for g in genre_ids.split(',') if g]
        if genre_list:
            query = query.filter(Book.genres.any(Genre.id.in_(genre_list)))
    if year_values:
        year_list = [int(y) for y in year_values.split(',') if y]
        if year_list:
            query = query.filter(Book.year.in_(year_list))
    if pages_from:
        query = query.filter(Book.pages >= pages_from)
    if pages_to:
        query = query.filter(Book.pages <= pages_to)
    
    # Order by newest first
    query = query.order_by(Book.year.desc(), Book.created_at.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=Config.BOOKS_PER_PAGE, error_out=False)
    books = pagination.items
    
    # Get data for filters (needed for dropdowns)
    all_genres = Genre.query.order_by('name').all()
    all_years = sorted(set([b.year for b in Book.query.all()]), reverse=True)
    
    return render_template('index.html', 
                         books=books, 
                         pagination=pagination,
                         genres=all_genres,
                         years=all_years)