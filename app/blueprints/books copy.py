from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app import db
from app.forms import BookForm, SearchForm
from app.models import Book, Genre, Cover, Review
from app.utils import save_cover, delete_cover_file, markdown_to_html
import os

books_bp = Blueprint('books', __name__)

def check_admin():
    if not current_user.is_authenticated or current_user.role.name not in ['admin', 'moderator']:
        flash('У вас недостаточно прав для выполнения данного действия', 'danger')
        return False
    return True

def check_admin_only():
    if not current_user.is_authenticated or current_user.role.name != 'admin':
        flash('У вас недостаточно прав для выполнения данного действия', 'danger')
        return False
    return True

@books_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not check_admin():
        return redirect(url_for('main.index'))
    
    form = BookForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.order_by('name').all()]
    
    if form.validate_on_submit():
        try:
            book = Book(
                title=form.title.data,
                description=form.description.data,
                year=form.year.data,
                publisher=form.publisher.data,
                author=form.author.data,
                pages=form.pages.data
            )
            db.session.add(book)
            db.session.flush()  # Get book ID
            
            # Add genres
            for genre_id in form.genres.data:
                genre = Genre.query.get(genre_id)
                if genre:
                    book.genres.append(genre)
            
            db.session.commit()
            
            # Save cover if provided
            if form.cover.data:
                save_cover(form.cover.data, book.id, db, Cover)
                db.session.commit()
            
            flash('Книга успешно добавлена!', 'success')
            return redirect(url_for('books.view_book', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            print(f"Error: {e}")
    
    return render_template('book_form.html', form=form, title='Добавление книги', is_edit=False)

@books_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not check_admin():
        return redirect(url_for('main.index'))
    
    book = Book.query.get_or_404(book_id)
    form = BookForm()
    form.genres.choices = [(g.id, g.name) for g in Genre.query.order_by('name').all()]
    
    if form.validate_on_submit():
        try:
            book.title = form.title.data
            book.description = form.description.data
            book.year = form.year.data
            book.publisher = form.publisher.data
            book.author = form.author.data
            book.pages = form.pages.data
            
            # Update genres
            book.genres = []
            for genre_id in form.genres.data:
                genre = Genre.query.get(genre_id)
                if genre:
                    book.genres.append(genre)
            
            db.session.commit()
            flash('Книга успешно обновлена!', 'success')
            return redirect(url_for('books.view_book', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            print(f"Error: {e}")
    else:
        # Populate form
        form.title.data = book.title
        form.description.data = book.description
        form.year.data = book.year
        form.publisher.data = book.publisher
        form.author.data = book.author
        form.pages.data = book.pages
        form.genres.data = [g.id for g in book.genres]
    
    return render_template('book_form.html', form=form, title='Редактирование книги', is_edit=True, book=book)

@books_bp.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if not check_admin_only():
        return redirect(url_for('main.index'))
    
    book = Book.query.get_or_404(book_id)
    try:
        # Delete cover file
        if book.cover:
            delete_cover_file(book.cover)
        
        db.session.delete(book)
        db.session.commit()
        flash(f'Книга "{book.title}" успешно удалена!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении книги', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('main.index'))

@books_bp.route('/view/<int:book_id>')
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    book.description_html = markdown_to_html(book.description)
    
    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(book_id=book.id, user_id=current_user.id).first()
    
    return render_template('book_detail.html', book=book, user_review=user_review)