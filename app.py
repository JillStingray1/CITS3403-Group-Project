from flask import Flask, redirect, url_for

app = Flask(__name__)

# Import after app is defined
import routes.routes  # this will import routes.py, which imports user and meeting


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

if __name__ == "__main__":
    app.run(debug=True)