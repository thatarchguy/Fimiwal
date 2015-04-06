from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Required, EqualTo
from fimiwal import models, db


class AddClient(Form):
    email = StringField(u'email', validators=[DataRequired()])
    ip = StringField(u'ip')
    ident = StringField(u'ident')
    directory = StringField(u'directory')
    os = SelectField(u'os',
                     choices=[('windows', 'Windows'), ('linux', 'GNU/Linux')],
                     validators=[DataRequired()])


class SettingsPass(Form):
    currentPass = PasswordField('currentpass', validators=[DataRequired()])
    newPass = PasswordField(
        'New Password', [Required(), EqualTo('newPassVerify',
                                             message='Passwords must match')])
    newPassVerify = PasswordField('Repeat Password')


class SettingsGeneral(Form):
    email = StringField(u'email', validators=[DataRequired()])
