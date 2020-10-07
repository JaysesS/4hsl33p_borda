from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, ValidationError
from wtforms.validators import InputRequired, Email, Length
import re
import requests as req

class RegisterForm(FlaskForm):

    class Meta:
        csrf = False

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    telegram = StringField("Telegram", validators=[InputRequired()])
    
    def validate_username(self, username):
        if bool(re.match("^[A-Za-z0-9_-]*$", username.data)) is False:
            raise ValidationError('Username love - ^[A-Za-z0-9_-]*$')
        if len(username.data) < 4:
            raise ValidationError('Username >= 4 characters..')
        elif len(username.data) > 10:
            raise ValidationError('Username <= 10 characters..')
    
    def validate_password(self, password):
        if bool(re.match("^[A-Za-z0-9_-]*$", password.data)) is False:
            raise ValidationError('Password love - ^[A-Za-z0-9_-]*$')
        if len(password.data) < 4:
            raise ValidationError('Password is >= 4 characters..')
        elif len(password.data) > 30:
            raise ValidationError('Password is <= 30 characters..')
    
    def validate_telegram(self, telegram):
        if bool(re.match("^[A-Za-z0-9_@-]*$", telegram.data)) is False and telegram.data[0] == '@':
            raise ValidationError('Enter as in this example - @jaysess')
        if str(telegram.data)[1:].strip() not in req.get("https://t.me/{}".format(str(telegram.data)[1:].strip())).text:
            raise ValidationError('Need valid user :c')

class LoginForm(FlaskForm):

    class Meta:
        csrf = False

    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    remember = BooleanField("Remember me")

    def validate_username(self, username):
        if bool(re.match("^[A-Za-z0-9_-]*$", username.data)) is False:
            raise ValidationError('Username love - ^[A-Za-z0-9_-]*$')
        if len(username.data) < 4:
            raise ValidationError('Username >= 4 characters..')
        elif len(username.data) > 10:
            raise ValidationError('Username <= 10 characters..')

    def validate_password(self, password):
        if bool(re.match("^[A-Za-z0-9_-]*$", password.data)) is False:
            raise ValidationError('Password love - ^[A-Za-z0-9_-]*$')
        if len(password.data) < 4:
            raise ValidationError('Password is >= 4 characters..')
        elif len(password.data) > 30:
            raise ValidationError('Password is <= 30 characters..')

class FlagForm(FlaskForm):

    class Meta:
        csrf = False
    
    answer = StringField("Flag", validators = [InputRequired()])

    def validate_answer(self, answer):
        if bool(re.match("^[A-Za-z0-9!?.-_{}'#&]*$", answer.data)) is False:
            raise ValidationError('Flag love - ^[A-Za-z0-9!?.-_{}\'#&]*$')
        if len(answer.data) < 10 or answer.data[:8] != "4hsl33p{" or answer.data[-1] != "}":
            raise ValidationError('The format of the flag - 4hsl33p{...}')