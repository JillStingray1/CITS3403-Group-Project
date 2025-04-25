from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from extensions import db
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = os.getenv('SESSION_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URI')

db.init_app(app)

# Import after app is defined
import models.Models

# after the models are imported, create the database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

from routes import user_routes, meeting_routes
user_routes.init_user_routes(app, db, bcrypt)
meeting_routes.init_meeting_routes(app, db)

if __name__ == "__main__":
    app.run(debug=True)