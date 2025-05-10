from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


class ShareCodeForm(FlaskForm):
    code = StringField(
        "Code",
        validators=[
            DataRequired(),
            Regexp(
                # This regex only works with $ at the end, despite the rest of the regex
                # meaning that only characters A-Z, a-z, 0-9 and _ can be used
                "[A-Za-z0-9]+$",
                message="Share Code not of the valid format",
            ),
        ],
    )
    submit = SubmitField("Import")
