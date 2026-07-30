from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
def create_app():
	app = Flask(__name__)
	app.config.update(SECRET_KEY="KEY_FAQ")
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bot_messenger.db"
	migrate = Migrate(app,db)
	db.init_app(app)
	from routes import register_routes
	register_routes(app,db)
	return app
