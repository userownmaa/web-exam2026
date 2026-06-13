// Confirm delete modal
function confirmDelete(bookId, bookTitle) {
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    document.getElementById('deleteBookId').value = bookId;
    document.getElementById('deleteBookTitle').textContent = bookTitle;
    modal.show();
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Form validation for pages range
function validatePagesRange() {
    const pagesFrom = document.getElementById('pages_from');
    const pagesTo = document.getElementById('pages_to');
    
    if (pagesFrom && pagesTo) {
        if (parseInt(pagesFrom.value) > parseInt(pagesTo.value)) {
            alert('Объём "от" не может быть больше объёма "до"');
            return false;
        }
    }
    return true;
}

// Search form submit handler
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            if (!validatePagesRange()) {
                e.preventDefault();
            }
        });
    }
});

// Rating stars display
function displayRating(rating) {
    const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
    return stars;
}