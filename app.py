from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

from flask_login import LoginManager
from datetime import timedelta

PERMANENT_SESSION_LIFETIME = timedelta(hours=3)


login_manager = LoginManager()
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
def create_app():
	app = Flask(__name__)
	app.config.from_object("config")
	app.config.update(SECRET_KEY="KEY_FAQ")
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bot_messenger_auto.db"
	app.json.ensure_ascii = False
	migrate = Migrate(app,db)
	db.init_app(app)

	login_manager.init_app(app)
	login_manager.login_view = "login"  # Đặt tên route cho trang đăng nhập
	from routes.routes import register_routes
	from routes.webhook import webhook_bp
	register_routes(app,db)
	app.register_blueprint(webhook_bp)
	return app
@login_manager.user_loader
def load_user(user_id):
	from models import User
	return db.session.get(User, int(user_id))