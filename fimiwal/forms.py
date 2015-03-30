from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Required, EqualTo
from fimiwal import models, db


class AddClient(Form):
    email           = StringField(u'email', validators=[DataRequired()])
    ip              = StringField(u'ip')
    ident           = StringField(u'ident')
    ssh             = StringField(u'ssh')


class SettingsPass(Form):
    currentPass     = PasswordField('currentpass', validators=[DataRequired()])
    newPass         = PasswordField('New Password', [Required(), EqualTo('newPassVerify', message='Passwords must match')])
    newPassVerify   = PasswordField('Repeat Password')


class SettingsGeneral(Form):
    email           = StringField(u'email', validators=[DataRequired()])
