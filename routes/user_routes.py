from flask import session, request, jsonify, redirect, url_for
from models.Models import User
from tools import validate_username, validate_password, save_login_session, clear_login_session
from middleware.middleware import secure


def init_user_routes(app, db, bcrypt):
    """
    Initialize the user routes for the app.
    Args:
        app (Flask): The Flask app to initialize the routes for.
        db (SQLAlchemy): The SQLAlchemy database instance to use.
    """
    # TODO: add authentication to the routes that require a user to be logged in. fill in the pass statements with the appropriate code. upon login, pass the user id to the session.
    print("User routes loaded")

    @app.route('/user', methods=['GET'])
    @secure   
    #this route will be used to get the user details of the logged in user, useful for loading the users meetings
    def get_user():
        return jsonify({
            "id": session['user_id'],
            "username": session['username'],
            "meeting": session['meeting_id']
        }), 200

    @app.route('/user/signup', methods=['POST'])
    def create_user():
        """
        Create a new user.
        Args:
            JSON { username: 'username', password: 'password'}

        Returns:
            On success, redurects to the main menu page and adds user to session.
            On failure, returns a JSON object with an error message and 400.

        """
        data = request.get_json()
        username = data.get('username')
        is_username_valid = User.query.filter(User.username == username).first()
        if is_username_valid is not None: 
            return jsonify({"error": "Username already exists"}), 400
        else:
            password = data.get('password')
            if validate_username(username) is False:
                return jsonify({"error": "Invalid username"}), 400
            if validate_password(password) is False:
                return jsonify({"error": "Invalid password"}), 400
            
            new_user = User(username=username, password_hash=bcrypt.generate_password_hash(password.encode('utf-8')))

            db.session.add(new_user)
            db.session.commit()

            save_login_session(new_user)
            # setting the session variables to the current user
            
            return redirect(url_for('static', filename='main-menu.html')) # redirect to the main menu page after signup

    @app.route('/user/login', methods=['POST'])
    def login_user():
        """
        login a user.

        Args:
            JSON { username: 'username', password: 'password'}

        Returns:
            On success, redurects to the main menu page adds user to session.
            On failure, returns a JSON object with an error message and 400.
        """
        if 'logged_in' in session and session['logged_in']:
            return redirect(url_for('static', filename='main-menu.html'))
        
        data = request.get_json()
        username = data.get('username')
        is_user = User.query.filter(User.username == username).first()
        if is_user is None:
            return jsonify({"error": "user not found"}), 400
        else: 
            password = data.get('password')
            if bcrypt.check_password_hash( is_user.password_hash, password):
            
                save_login_session(is_user)

                return redirect(url_for('static', filename='main-menu.html')), 200 # redirect to the main menu page after successful login
            else:
                return jsonify({"error": "Invalid password"}), 400


    @app.route('/user/logout', methods=['GET'])
    @secure   
    def logout_user():
        """
        Logout a user. Redirects to the index page.
        """
        clear_login_session()
        return redirect(url_for('static', filename='index.html')), 200
    

