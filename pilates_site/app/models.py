from flask_login import UserMixin
from .import db
from werkzeug.security import generate_password_hash, check_password_hash

# Many-to-Many relationship table for favorites
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('link_id', db.Integer, db.ForeignKey('category_link.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    # Relationship with favorites
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    
    def is_admin(self):
        return self.role == 'admin'

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.role = role
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class CategoryLink(db.Model):
    __tablename__ = 'category_links'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    category = db.relationship('Category', backref=db.backref('links', lazy=True))

    def __repr__(self):
        return f"CategoryLink(title={self.title}, url={self.url})"

class Favorite(db.Model):
    __tablename__ = 'favorites'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('category_link.id'), primary_key=True)

    def __repr__(self):
        return f'<Favorite user_id={self.user_id}, link_id={self.link_id}>'
