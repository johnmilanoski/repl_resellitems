from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from app import db
from models import User, Listing
from forms import AdminUserForm, AdminListingForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            current_app.logger.warning(f"Non-admin user {current_user.id} attempted to access admin panel")
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@admin_required
def admin_panel():
    current_app.logger.info(f"Admin panel accessed by user {current_user.id}")
    users = User.query.all()
    listings = Listing.query.all()
    return render_template('admin/panel.html', users=users, listings=listings)

@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        user.enable_cross_platform_posting = form.enable_cross_platform_posting.data
        db.session.commit()
        current_app.logger.info(f"User {user_id} updated by admin {current_user.id}")
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/listing/<int:listing_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    form = AdminListingForm(obj=listing)
    if form.validate_on_submit():
        listing.title = form.title.data
        listing.description = form.description.data
        listing.price = form.price.data
        listing.location = form.location.data
        listing.negotiable = form.negotiable.data
        listing.status = form.status.data
        db.session.commit()
        current_app.logger.info(f"Listing {listing_id} updated by admin {current_user.id}")
        flash('Listing updated successfully.', 'success')
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin/edit_listing.html', form=form, listing=listing)

@admin.route('/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('You cannot delete your own account.', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        current_app.logger.info(f"User {user_id} deleted by admin {current_user.id}")
        flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.admin_panel'))

@admin.route('/listing/<int:listing_id>/delete', methods=['POST'])
@admin_required
def admin_delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    db.session.delete(listing)
    db.session.commit()
    current_app.logger.info(f"Listing {listing_id} deleted by admin {current_user.id}")
    flash('Listing deleted successfully.', 'success')
    return redirect(url_for('admin.admin_panel'))
