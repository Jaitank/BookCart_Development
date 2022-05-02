from cProfile import label
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms.validators import Length, EqualTo, Email, DataRequired



class RegisterFrom(FlaskForm):
    
    username = StringField(label='User Name:', validators = [Length(min=2, max=20), DataRequired()] )
    email_address = StringField(label = 'Email Address:',validators = [Email(), DataRequired()] )
    password1 = PasswordField(label = 'Password:',validators = [Length(min=6), DataRequired()] )
    password2 = PasswordField(label = 'Confirm Password:',validators = [EqualTo('password1'), DataRequired()] )
    submit = SubmitField(label = 'Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators = [DataRequired()] )
    password = PasswordField(label = 'Password:',validators = [ DataRequired()] )
    submit = SubmitField(label='Sign In')


class sellingForm(FlaskForm):
    streamName = SelectField(label='Book Stream', choices=['JEE', 'School','NEET','B.Tech'],validate_choice=[DataRequired()])
    bookname = StringField(label= 'Book Name:', validators=[Length(min=4, max=30),DataRequired()])
    subjectName = StringField(label= 'Subject Name :', validators=[Length(min=4, max=20), DataRequired()])
    className = IntegerField(label= 'Class:',validators=[DataRequired()])
    mfgYear = IntegerField(label= 'Manufacturing Year:', validators=[DataRequired()])
    sellingAmount = IntegerField(label= 'Selling Amount:', validators=[DataRequired()])
    publicationName = StringField(label= 'Publication Name :', validators=[Length(min=2, max=20),DataRequired()])
    bookImage = FileField(label = 'Book Image: ', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    quantity = IntegerField(label='Qunatity: ', validators=[DataRequired()])
    submit = SubmitField(label='Add Book')




