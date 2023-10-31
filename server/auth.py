from flask import Blueprint, flash, render_template, request, url_for, redirect, Response
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db

import typing

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> (Response | str):
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):
        #get username, password and email from the form
        fname = register.f_name.data
        lname = register.l_name.data
        pwd = register.password.data
        email = register.email_id.data
        pnum = register.p_number.data
        #check if a user exists
        user = db.session.scalar(db.select(User).where(User.emailid==email))
        number = pnum.replace(" ", "")
        if((not len(number)==10) or (not number.isnumeric())):
            flash('Invalid phone number')
            return redirect(url_for('auth.register'))
        if user:#this returns true when user is not None
            flash('An account already exists for this email address.')
            return redirect(url_for('auth.register'))
        
        # don't store the password in plaintext!
        pwd_hash = generate_password_hash(pwd)
        #create a new User model object
        new_user = User(fname=fname, lname = lname, pnumber = number, password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        #commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register, heading='Register')


# this is the hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
def authenticate() -> (Response | None | str): #view function
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        email = login_form.email.data
        password = login_form.password.data
        u1 = User.query.filter_by(emailid=email).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            return redirect(url_for('main.index'))
            #nextp = request.args.get('next') #this gives the url from where the login page was accessed
            #print(nextp)

            '''
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
            return redirect(nextp)
            '''
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@auth_bp.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('main.index'))