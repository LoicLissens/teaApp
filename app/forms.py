from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from wtforms.fields.html5 import EmailField
import email_validator
from app.models import User, Tea, Region, Type


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password Vérification',
                              validators=[DataRequired(), EqualTo('password')])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    #remember_me = BooleanField()
    submit = SubmitField('Register !')
    # When you add any methods that match the pattern validate_<field_name>, WTForms takes those as custom validators and invokes them in addition to the stock validators.

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError(
                "T'es carrote, qq'un a déjà pris ton pseudo !")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data.lower()).first()
        if email is not None:
            raise ValidationError('Please use a different email address.')


class AddTeaForm(FlaskForm):
    teaname = StringField('Tea name', validators=[DataRequired()])
    description = TextAreaField('Description')
    region = SelectField('Comes from', choices=Region.reg_list_to_tupple())
    type = SelectField('Type of tea', choices=Type.type_list_to_tupple())
    water_temp = StringField("Temperature of water(Deg Celsius)")
    water_time = StringField("Infusion time(Minutes)")
    submit = SubmitField('Add this tea !')

    def validate_teaname(self, teaname):
        name = Tea.query.filter_by(name=teaname.data.lower()).first()
        if name is not None:
            raise ValidationError('This tea is already registered ')


class AddFunFactForm(FlaskForm):
    fun_fact_fr = TextAreaField("Fun fact FR", validators=[DataRequired()])
    fun_fact_en = TextAreaField("Fun fact EN", validators=[DataRequired()])
    submit = SubmitField('Add this fun fact')
