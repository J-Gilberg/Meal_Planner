from flask_app import app
from flask_app.models import user
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')


@app.route('/register/user', methods=['POST'])
def register():

    if not user.User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'username': request.form['username'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session['user_id'] = user.User.save(data)
    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["login_email"]}
    user_in_db = user.User.get_by_email(data)
    if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id
    print(session['user_id'])
    # never render on a post!!!
    return redirect("/dashboard")



