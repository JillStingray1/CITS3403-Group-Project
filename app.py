from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from extensions import db
from dotenv import load_dotenv
from routes import user_routes, meeting_routes
import os

from flask_login import LoginManager
from models import User  # your User model

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login_user'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SECRET_KEY'] = os.getenv('SESSION_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URI')
CSRFProtect(app)

db.init_app(app)
migrate = Migrate(app, db)

# Import after app is defined
import models.Models

# after the models are imported, create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template("index.html")


user_routes.init_user_routes(app, db, bcrypt)
meeting_routes.init_meeting_routes(app, db)

if __name__ == "__main__":
    app.run(debug=True)
