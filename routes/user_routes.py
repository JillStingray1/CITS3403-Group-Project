from flask import (
    session,
    request,
    jsonify,
    redirect,
    url_for,
    render_template,
)
from models import User
from tools import save_login_session, clear_login_session
from middleware.middleware import secure
from forms import LoginForm, SignUpForm


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
    # this route will be used to get the user details of the logged in user, useful for loading the users meetings
    def get_user():
        return jsonify({
            "id": session['user_id'],
            "username": session['username'],
            "meeting": session['meeting_id']
        }), 200

    @app.route("/user/signup", methods=["GET", "POST"])
    def signup():
        """
        Renders the signup template and redirects to other menus

        Returns:
            On success, redirects to the main menu page and adds user to session.
            On failure, returns a JSON object with an error message and 400.

        """
        form = SignUpForm()
        if form.validate_on_submit():
            # Password and Username cannot be null since they have the data required validator
            username = form.username.data
            is_username_valid = User.query.filter(User.username == username).first()
            if is_username_valid is not None:
                return render_template("sign-up.html", form=form, is_username_valid=False)
            password = form.password.data
            new_user = User(username=username, password_hash=bcrypt.generate_password_hash(password.encode("utf-8")))  # type: ignore

            db.session.add(new_user)
            db.session.commit()

            save_login_session(new_user)
            # setting the session variables to the current user
            return redirect("/main-menu")  # redirect to the main menu page after signup
        return render_template("sign-up.html", form=form, is_username_valid=True)

    @app.route("/user/login", methods=["GET", "POST"])
    def login():
        """
        Renders the login template and redirects to other menus

        Returns:
            On success, redirects to the main menu page and adds user to session.
            On failure, returns a JSON object with an error message and 400.

        """
        if "user_id" in session:
            return redirect(url_for("main_menu"))
        form = LoginForm()
        if form.validate_on_submit():
            # Password and Username cannot be null since they have the data required validator
            username = form.username.data
            user = User.query.filter(User.username == username).first()
            if user is None:
                return render_template("login.html", form=form, error="User does not exist.")
            password = form.password.data
            if bcrypt.check_password_hash(user.password_hash, password):
                save_login_session(user)
                return redirect("/main-menu")
            return render_template("login.html", form=form, error="Incorrect Password.")

            # setting the session variables to the current user
        return render_template("login.html", form=form, error=None)

    @app.route('/user/logout', methods=['GET'])
    @secure   
    def logout_user():
        """
        Logout a user. Redirects to the index page.
        """
        clear_login_session()
        return render_template("index.html"), 200
