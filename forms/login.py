from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=25, message="Username must be between 3 to 25 characters"),
            Regexp(
                # This regex only works with $ at the end, despite the rest of the regex
                # meaning that only characters A-Z, a-z, 0-9 and _ can be used
                "[A-Za-z0-9_]+$",
                message="Username must contain only alphanumeric characters and _",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=5, max=35, message="Password must be between 5 to 35 characters"),
            Regexp(
                # Similar to above
                "[A-Za-z0-9!#+:=.?]+$",
                message="Password must contain only alphanumeric characters and the following special characters !#+:=.?",
            ),
        ],
    )
    submit = SubmitField("Login")
