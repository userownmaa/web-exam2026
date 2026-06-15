from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import ReviewForm
from app.models import Review, Book
from app.utils import sanitize_html

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/add/<int:book_id>', methods=['GET', 'POST'])
@login_required
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    
    existing_review = Review.query.filter_by(book_id=book.id, user_id=current_user.id).first()
    if existing_review:
        flash('Вы уже оставили рецензию на эту книгу', 'warning')
        return redirect(url_for('books.view_book', book_id=book.id))
    
    form = ReviewForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                review = Review(
                    book_id=book.id,
                    user_id=current_user.id,
                    rating=form.rating.data,
                    text=sanitize_html(form.text.data)
                )
                db.session.add(review)
                db.session.commit()
                flash('Рецензия успешно добавлена!', 'success')
                return redirect(url_for('books.view_book', book_id=book.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при сохранении рецензии: {str(e)}', 'danger')
                print(f"Error saving review: {e}")
        else:
            if form.errors and any(form.errors.values()):
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'Ошибка в поле {field}: {error}', 'danger')
    
    return render_template('review_form.html', form=form, book=book)