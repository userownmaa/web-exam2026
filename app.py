from app import create_app, db
from app.models import User, Role, Genre, Book, Cover, Review

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Genre': Genre,
        'Book': Book,
        'Cover': Cover,
        'Review': Review
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)