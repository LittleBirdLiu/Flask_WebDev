from flask import render_template, abort, redirect, flash, url_for
from ..models import User,Role
from . import main
from .forms import EditProfileForm, AdminEditProfileForm
from flask_login import login_required, current_user
from app import db


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/edit-Profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('the profile have been changed ')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-Profile/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = AdminEditProfileForm(user= user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.name = form.name.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('the profile have been changed ')
        return redirect(url_for('.user', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.username.data = user.username
    form.email.data = user.email
    form.role.data = user.role
    form.confirmed.data = user.confirmed
    return render_template('edit_profile.html', form=form, user=user)