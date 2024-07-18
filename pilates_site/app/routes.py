from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.exceptions import NotFound
from app.models import User, Category, CategoryLink
from app import db
from app.forms import CategoryLinkForm
from app.models import Favorite

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.index'))
        flash('Invalid credentials')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')  # Role, formdan alınır, varsayılan 'user' olarak ayarlanır
        
        # Yeni kullanıcı oluşturup veritabanına kaydet
        new_user = User(username=username, email=email, role=role, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page')
        return redirect(url_for('routes.index'))
    return render_template('admin.html')

@bp.route('/admin/category_link/add', methods=['GET', 'POST'])
@login_required
def add_category_link():
    form = CategoryLinkForm()

    if form.validate_on_submit():
        title = form.title.data
        url = form.url.data
        category_id = form.category_id.data

        new_link = CategoryLink(title=title, url=url, category_id=category_id)
        db.session.add(new_link)
        db.session.commit()

        flash('Link başarıyla eklendi.', 'success')
        return redirect(url_for('routes.index'))

    return render_template('add_category_link.html', form=form)

@bp.route('/category/<int:category_id>')
def category(category_id):
    if category_id == 1:
        return render_template('isinma.html')
    elif category_id == 2:
        return render_template('karin.html')
    elif category_id == 3:
        return render_template('bacak.html')
    elif category_id == 4:
        return render_template('kol.html')
    elif category_id == 5:
        return render_template('tum_vucut.html')
    elif category_id == 6:
        return render_template('sikca_sorulan_sorular.html')
    else:
        return render_template('404.html') 

@bp.route('/test_db')
def test_db():
    try:
        categories = Category.query.all()
        category_names = [category.name for category in categories]
        return {'categories': category_names}
    except Exception as e:
        return {'error': str(e)}

# Kullanıcı profilini görüntüleme
@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Kullanıcı profilini güncelleme
@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    
    if username and email:
        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash('Profiliniz güncellendi.')
    else:
        flash('Tüm alanları doldurmalısınız.')
    
    return redirect(url_for('routes.profile'))

# Kullanıcının favori egzersizlerini görüntüleme
@bp.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    if request.method == 'POST':
        selected_lessons = request.form.getlist('favorites')
        for lesson_id in selected_lessons:
            if not Favorite.query.filter_by(user_id=current_user.id, link_id=lesson_id).first():
                favorite = Favorite(user_id=current_user.id, link_id=lesson_id)
                db.session.add(favorite)
        db.session.commit()
        return redirect(url_for('routes.favorites'))

    categories = {}
    category_objs = Category.query.all()
    for category in category_objs:
        categories[category.name] = category.lessons

    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', categories=categories, favorites=favorites)

@bp.route('/toggle_favorite/<int:link_id>', methods=['GET'])
@login_required
def toggle_favorite(link_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, link_id=link_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
    return redirect(url_for('favorites'))


## yeni


@bp.route('/users', methods=['GET'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('routes.users'))
    
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('routes.users'))
    
    return render_template('edit_user.html', user=user)

@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    return redirect(url_for('routes.users'))


#ders ekleme
@bp.route('/add_to_program/<day>', methods=['POST'])
def add_to_program(day):
    if request.method == 'POST':
        category_links = CategoryLink.query.all()
        category_link_id = request.form.get('category_link_id')
        return redirect(url_for('routes.weekly_programs')) 
    
# hata kodları

def custom_errorhandler(code):
    def decorator(f):
        @bp.errorhandler(code)
        def handler(error):
            return f(error)
        return handler
    return decorator


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('routes.404.html'), 404

@bp.errorhandler(500)
def internal_server_error(error):
    return render_template('routes.500.html'), 500
    