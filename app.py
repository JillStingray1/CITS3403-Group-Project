from flask import Flask, redirect, url_for
from extensions import db
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SESSION_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URI')

db.init_app(app)

# Import after app is defined
import models.Models
import routes.routes  # this will import routes.py, which imports user and meeting

# after the models are imported, create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

if __name__ == "__main__":
    app.run(debug=True)