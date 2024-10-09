from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, BooleanField, PasswordField, SubmitField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CustomFieldForm(FlaskForm):
    name = StringField('Field Name')
    value = StringField('Field Value')

class ListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    negotiable = BooleanField('Price Negotiable')
    custom_fields = FieldList(FormField(CustomFieldForm), min_entries=1)
    submit = SubmitField('Create Listing')

class AdminUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_admin = BooleanField('Admin')
    enable_cross_platform_posting = BooleanField('Enable Cross-Platform Posting')
    submit = SubmitField('Update User')

class AdminListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    negotiable = BooleanField('Price Negotiable')
    status = SelectField('Status', choices=[('active', 'Active'), ('sold', 'Sold'), ('deleted', 'Deleted')])
    submit = SubmitField('Update Listing')

class AdminSearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')