"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app) 

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Shows home page"""
    return redirect("/users")

"""Routes"""
@app.route('/users')
def users_index():

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Create new user"""

    return render_template('users/new.html')

@app.route("/users/new", method=["POST"])
def users_new():
    """form submission"""
    
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def users_show(user_id):
    """Show information about a given user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route("/users/<int:user_id>")
def users_edit(user_id):
    """Show form to edit current user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route("/users/<int:user_id>", method=["POST"])
def users_edit(user_id):
    """Process the edit form, return the user to the /users page."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

app.route("users/<int:user_id>/delete", methods=['POST'])
def users_delete(user_id):
    """Handle form submission to delete existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")