from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

# Import after app is defined
import models.Models
import routes.routes  # this will import routes.py, which imports user and meeting



@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

if __name__ == "__main__":
    app.run(debug=True)