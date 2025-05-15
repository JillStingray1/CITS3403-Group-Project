from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, NumberRange
from datetime import date


class meetingCreationForm(FlaskForm):

    def validate_meeting_length(form, field):
        if field.data % 15 != 0:
            raise ValidationError("Meeting length must be divisible by 15 minutes")
        
    def validate_start_date(form, field):
        if field.data < date.today():
            raise ValidationError("Start date cannot be in the past")
        
    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            raise ValidationError("End date must be after start date")

    meeting_name = StringField(
        "Meeting Name",
        validators=[
            Length(
                max=80, message="Meeting name must be less than 80 characters"
            ),
            DataRequired(),
        ],

    )
    meeting_description = StringField(
        "Meeting Description",
        validators=[
            Length(
                max=2400, message="Meeting description must be less than 2400 characters"
            ),
            DataRequired(),
        ],

    )
    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="Start date is required"),
            validate_start_date
        ],
        render_kw={
            "min": date.today().isoformat()
        }
    )
    end_date = DateField(
        "End Date",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="End date is required"),
            validate_end_date,
        ],
        render_kw={
            "min": date.today().isoformat()
        }
    )
    meeting_length = IntegerField(
        "Meeting Length",
        validators=[
            DataRequired(message="Meeting length is required"),
            validate_meeting_length,
            NumberRange(min=15, max=300, message="Meeting length must be between 15 and 300 minutes"),
        ],
    )
    submit = SubmitField("Create Meeting")
