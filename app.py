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
	app.json.ensure_ascii = False
	migrate = Migrate(app,db)
	db.init_app(app)
	from routes.routes import register_routes
	from routes.webhook import webhook_bp
	register_routes(app,db)
	app.register_blueprint(webhook_bp)
	return app
