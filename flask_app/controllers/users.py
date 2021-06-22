from flask import render_template,redirect,request,flash,session
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/user',methods=['GET', 'POST'])
def register():
    if not user.User.validate(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {}
    data.update(request.form)
    data['password'] = pw_hash
    user.User.add_one(data)
    return redirect('/')


@app.route('/login/user', methods=['GET', 'POST'])
def login():
    if not user.User.validate(request.form):
        return redirect('/')
    print(request.form['email'])
    user_in_db = user.User.get_by_email({'email':request.form['email']})
    if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password","login")
        return redirect('/')
    for key,val in user_in_db.__dict__.items():
        session[key] = val
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')