from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from tools.extensions import db
from tools.config import DeploymentConfig


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    CSRFProtect(app)
    return app


app = create_app(DeploymentConfig)
bcrypt = Bcrypt(app)
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
