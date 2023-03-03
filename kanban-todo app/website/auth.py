
from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,current_user
from flask_login import login_required




auth = Blueprint('auth', __name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            flash("Logged in successfully",category="success")
            login_user(user,remember=True)

            return redirect(url_for('views.home'))
        else:
            flash('Invalid Credentials',category='error')
            return redirect(url_for('auth.login'))

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sgin_up():
    if request.method == 'POST':
        email = request.form.get('Email')
        username=request.form.get('Name')
        password1=request.form.get('password')
        password2=request.form.get('password2')

        if len(email) < 6:
            flash("Email is too short",category="error")
        elif len(username)<2:
            flash("Username is too short",category="error")
        elif password1 != password2:
            flash("Passwords do not match",category="error")
        elif len(password1)<6:
            flash("Password is too short",category="error")
        else:
            new_user=User(email=email,username=username,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("You are signed up",category="success")
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html",user=current_user)