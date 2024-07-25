from flask import Flask, render_template, redirect, flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "verysecret"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """ Homepage; Redirects to register """

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Shows form to create new user & handles form submission """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username,password,email,first_name,last_name)
        
        db.session.add(new_user)
        db.session.commit()
        session['user-id'] = username
        flash('Successfully Created User')

        return redirect('/secret')
    else:
        return render_template('register.html', form=form)

