# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError


class SameAs:
    def __init__(self, other_field):
        self.other_field = other_field

    def __call__(self, form, field):
        value = getattr(form, self.other_field).data
        if value != field.data:
            raise ValidationError("Confirmation must match password")


class CreateInviteForm(Form):
    # TODO: login name should replace the creator field
    creator = StringField('Creator')
    created_for_mail = StringField('Create for email',
                                   validators=[DataRequired()])


class RedeemForm(Form):
    last_name = StringField('Last name', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(),
                                                 SameAs("password")])
