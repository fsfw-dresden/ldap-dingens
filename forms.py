from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class CreateInviteForm(Form):
    # TODO: login name should replace the creator field
    creator = StringField('Creator')
    created_for_mail = StringField('Create for email',
                                   validators=[DataRequired()])


class RedeemForm(Form):
    last_name = StringField('Last name', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
