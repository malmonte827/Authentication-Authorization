from flask import Flask, render_template, redirect, flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm


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
        session['username'] = new_user.username
        flash('Successfully Created User')

        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ show login form & handles login """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
    
        if user:
            flash(f'Welcome back {user.username}!')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors=['Invalid username/password']

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    if 'username' not in session or username != session['username']:
        flash('You must be logged in to view!')
        return redirect('/login')

    user = User.query.get(username)
    form = RegisterForm()
    return render_template('show.html', user=user, form= form)
    

@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye!')
    return redirect('/')

@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    """ Deletes user & redirect to login """

    if "username" not in session or username != session['username']:
        flash('You must be logged in to view!')
        return redirect('/login')

    user = User.query.get(username)

    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods=['GET', 'POST'])
def new_feedback(username):
    """ Show add feedback form and handle Submission """

    if "username" not in session or username != session['username']:
        flash('You must be logged in to view!')
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("/new.html", form=form)
    

@app.route("/feedback/<int:feedback_id>/update", methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Show update feedback form & handle submission"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash('You must be logged in to view!')
        return redirect('/login')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash('You must be logged in to view!')
        return redirect('/login')

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")