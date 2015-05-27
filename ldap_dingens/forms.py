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


def ldap_uid(form, field):
    valid_chars = set("abcdefghijklmnopqrstuvwxyz")
    # we for now only allow ascii lower case
    s = field.data
    if any(c not in valid_chars for c in s):
        raise ValidationError("User name must only contain lower case "
                              "ascii characters")


class CreateInviteForm(Form):
    # TODO: login name should replace the creator field
    creator = StringField('Creator')
    created_for_mail = StringField('Create for email',
                                   validators=[DataRequired()])


class RedeemForm(Form):
    loginname = StringField('Login name', validators=[ldap_uid])
    displayname = StringField('Display name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(),
                                                 SameAs("password")])


class LoginForm(Form):
    loginname = StringField('Login name', validators=[ldap_uid])
    password = PasswordField('Password', validators=[DataRequired()])


class PasswdForm(Form):
    current_password = PasswordField(
        'Current password',
        validators=[DataRequired()])
    new_password = PasswordField(
        'New password',
        validators=[DataRequired()])
    confirm_new_password = PasswordField(
        'Confirm new password',
        validators=[DataRequired(),
                    SameAs("new_password")])
