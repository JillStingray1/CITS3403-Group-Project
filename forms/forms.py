from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class SignUpForm(FlaskForm):
    fullname = StringField("Full Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(min=5),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Sign Up")
