from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,\
    PasswordField, \
    SubmitField, \
    BooleanField,\
    IntegerField, \
    TextAreaField, \
    SelectField, \
    SelectMultipleField, \
    FloatField,\
    RadioField


from wtforms.validators import DataRequired, \
    Length, Email, EqualTo, ValidationError
from artwork.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# TODO: create here your forms
class ArtworkForm(FlaskForm):
    name = TextAreaField('Name of artwork', validators=[DataRequired()])
    category = SelectField('Category',
                           choices=[],
                           coerce=int, validators=[DataRequired()])
    time = FloatField('Time (1 - 80 Hours)', validators=[DataRequired()])
    color = RadioField('Color',
                        choices=[(1, 'Photography'), (2, 'Digital'), (3, 'Pencils'), (4, 'Markers'), (5, 'Ink'), (6, 'Charcoal'), (7, 'Gouache'), (8, 'Watercolors'), (9, 'Acrylic'), (10, 'Oil')],
                        coerce=int, validators=[DataRequired()])
    base = RadioField('Base',
                      choices=[(1, 'Poster'), (2, 'Paper'), (3, 'Canvas')],
                      coerce=int, validators=[DataRequired()])
    size = RadioField('Size',
                      choices=[(1, 'A5'), (2, 'A4'), (3, 'A3'), (4, 'A2'), (5, 'A1'),(6, 'F1'), (7, 'F10'), (8, 'F15'), (9, 'F25'), (10, 'F40')],
                      coerce=int, validators=[DataRequired()])
    frame = RadioField('Frame',
                       choices=[(1, 'Without Frame'), (2, 'With Frame')],
                       coerce=int, validators=[DataRequired()])
    image_file = FileField('Choose artwork image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


class BidForm(FlaskForm):
    bid = FloatField('', validators=[DataRequired()])
    submit = SubmitField('Place your bid')


