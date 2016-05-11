from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,PasswordField,TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username=StringField('username',validators=[DataRequired()])
	userpassword=PasswordField('userpassword',validators=[DataRequired()])

class EditForm(Form):
	blogtilte=StringField('blogtilte',validators=[DataRequired()])
	blogbody=TextAreaField('blogbody',validators=[DataRequired()])

class PlForm(Form):
	plbody=StringField('plbody',validators=[DataRequired()])
