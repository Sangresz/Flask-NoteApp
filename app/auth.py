from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Users
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash("You can't login while still logged in, sign out please",
              category="error")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email is None or password is None:
            flash("You didn't type one of the required input", category="error")

        else:
            user = Users.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully", category="success")
                    login_user(user)
                    return redirect(url_for('views.home'))
                else:
                    flash("The password is wrong", category="error")
            else:
                flash("The email is wrong", category="error")

    return render_template('login.html', user=current_user)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        flash("You can't register a new user while still logged in, sign out please", category="error")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('user')
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')

        if len(email) < 1 or len(username) < 1 or len(password) < 1 or len(conf_password) < 1:
            flash("You didn't type one of the required input", category="error")
        elif len(email) > 254:
            flash("The email is too long")
        elif len(username) > 49:
            flash("The user is too long")
        elif len(username) > 254:
            flash("The password is too long")
        elif password != conf_password:
            flash("Your password don't match", category="error")
        else:
            user = Users.query.filter_by(email=email).first()
            if not user:
                new_user = Users(email=email, username=username,
                                 password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()

                flash("Account created and logged automatically",
                      category="success")
                login_user(new_user)
                return redirect(url_for('views.home'))
            else:
                flash(
                    "There is already an account with this email. Please login on this page", category="error")
                return redirect(url_for('auth.login'))

    return render_template('register.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", category="success")
    return redirect(url_for('auth.login'))
