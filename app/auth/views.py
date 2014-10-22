from flask import render_template, request, flash, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask.ext.babel import gettext as _

from app.model import User, Permission
from . import auth

class LoginForm(Form):
    username = StringField(_("Username"), validators=[DataRequired(), Length(3,128)])
    password = PasswordField(_("Password"), validators=[DataRequired()])
    submit = SubmitField(_("Log in"))


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            if user.can(Permission.WEB_ACCESS):
                login_user(user)
                return redirect(request.args.get('next') or url_for('root.index'))
            else:
                flash(_("User not permitted to access the web client"))
        else:
            flash(_("Invalid username or password"))

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_("Session terminated"))
    return redirect(url_for('root.index'))

    