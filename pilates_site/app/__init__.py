from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
mysql = MySQL()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # MySQL bağlantı ayarları
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'admin'
    app.config['MYSQL_PASSWORD'] = 'Kahraman.55'
    app.config['MYSQL_DB'] = 'pilates_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Kahraman.55@localhost/pilates_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    mysql.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Blueprint'leri kaydetme
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)


    # Kullanıcı yükleme fonksiyonunu tanımlama
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app, mysql, login_manager, db
