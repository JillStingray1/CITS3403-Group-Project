from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from extensions import db
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = os.getenv('SESSION_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URI')
CSRFProtect(app)

db.init_app(app)
migrate = Migrate(app, db)

# Import after app is defined
import models

# after the models are imported, create the database tables
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")

from routes import user_routes, meeting_routes
user_routes.init_user_routes(app, db, bcrypt)
meeting_routes.init_meeting_routes(app, db)

if __name__ == "__main__":
    app.run(debug=True)
