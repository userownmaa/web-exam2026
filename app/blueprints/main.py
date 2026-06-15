from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from app.models import Book, Genre, Review
from sqlalchemy import or_, and_
from config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    query = Book.query
    
    title = request.args.get('title', '').strip()
    author = request.args.get('author', '').strip()
    genre_ids = request.args.get('genre', '')
    year_values = request.args.get('year', '')
    pages_from = request.args.get('pages_from', '', type=int)
    pages_to = request.args.get('pages_to', '', type=int)
    
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
    
    query = query.order_by(Book.year.desc(), Book.created_at.desc())
    
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=Config.BOOKS_PER_PAGE, error_out=False)
    books = pagination.items
    
    all_genres = Genre.query.order_by('name').all()
    all_years = sorted(set([b.year for b in Book.query.all()]), reverse=True)
    
    return render_template('index.html', 
                         books=books, 
                         pagination=pagination,
                         genres=all_genres,
                         years=all_years)