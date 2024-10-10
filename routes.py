import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models import Listing, Photo, CustomField, User, Notification
from forms import ListingForm, CustomFieldForm
from external_platforms import post_to_external_platforms, check_external_platforms_comments

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

@main.route('/')
@main.route('/home')
def index():
    listings = Listing.query.filter_by(status='active').order_by(Listing.id.desc()).limit(10).all()
    return render_template('index.html', listings=listings)

@main.route('/my_listings')
@login_required
def my_listings():
    listings = current_user.listings.order_by(Listing.id.desc()).all()
    return render_template('my_listings.html', listings=listings)

@main.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    form = ListingForm()
    if form.validate_on_submit():
        try:
            listing = Listing(
                title=form.title.data,
                description=form.description.data,
                price=form.price.data,
                location=form.location.data,
                negotiable=form.negotiable.data,
                user_id=current_user.id
            )
            db.session.add(listing)
            db.session.flush()

            for photo in request.files.getlist('photos'):
                if photo and allowed_file(photo.filename):
                    filename = secure_filename(photo.filename)
                    photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    photo.save(photo_path)
                    photo_db = Photo(filename=filename, listing_id=listing.id)
                    db.session.add(photo_db)
                    current_app.logger.info(f"Photo saved: {photo_path}")
                else:
                    current_app.logger.warning(f"Invalid file: {photo.filename}")

            for field in form.custom_fields.data:
                if field['name'] and field['value']:
                    custom_field = CustomField(name=field['name'], value=field['value'], listing_id=listing.id)
                    db.session.add(custom_field)

            db.session.commit()

            if current_user.enable_cross_platform_posting:
                external_results = post_to_external_platforms(listing)
                for result in external_results:
                    if result['success']:
                        flash(f"Successfully posted to {result['platform']}!")
                    else:
                        flash(f"Failed to post to {result['platform']}: {result['error']}", 'error')
            else:
                flash('Cross-platform posting is disabled. Your listing was only created on this platform.')

            flash('Your listing has been created!', 'success')
            return redirect(url_for('main.view_listing', listing_id=listing.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating listing: {str(e)}")
            flash('An error occurred while creating your listing. Please try again.', 'error')

    return render_template('create_listing.html', form=form)

@main.route('/listing/<int:listing_id>')
def view_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    check_external_platforms_comments(listing)
    return render_template('view_listing.html', listing=listing)

@main.route('/listing/<int:listing_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.user_id != current_user.id:
        flash('You can only edit your own listings.', 'error')
        return redirect(url_for('main.view_listing', listing_id=listing_id))

    form = ListingForm(obj=listing)

    if form.validate_on_submit():
        try:
            listing.title = form.title.data
            listing.description = form.description.data
            listing.price = form.price.data
            listing.location = form.location.data
            listing.negotiable = form.negotiable.data

            for photo in request.files.getlist('photos'):
                if photo and allowed_file(photo.filename):
                    filename = secure_filename(photo.filename)
                    photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    photo.save(photo_path)
                    photo_db = Photo(filename=filename, listing_id=listing.id)
                    db.session.add(photo_db)
                    current_app.logger.info(f"Photo saved: {photo_path}")
                else:
                    current_app.logger.warning(f"Invalid file: {photo.filename}")

            # Clear existing custom fields
            CustomField.query.filter_by(listing_id=listing.id).delete()

            # Add updated custom fields
            for field in form.custom_fields.data:
                if field['name'] and field['value']:
                    custom_field = CustomField(name=field['name'], value=field['value'], listing_id=listing.id)
                    db.session.add(custom_field)

            db.session.commit()

            if current_user.enable_cross_platform_posting:
                external_results = post_to_external_platforms(listing)
                for result in external_results:
                    if result['success']:
                        flash(f"Successfully updated listing on {result['platform']}!", 'success')
                    else:
                        flash(f"Failed to update listing on {result['platform']}: {result['error']}", 'error')
            else:
                flash('Cross-platform posting is disabled. Your listing was only updated on this platform.', 'info')

            flash('Your listing has been updated!', 'success')
            return redirect(url_for('main.view_listing', listing_id=listing.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating listing {listing_id}: {str(e)}")
            flash('An error occurred while updating your listing. Please try again.', 'error')

    return render_template('edit_listing.html', form=form, listing=listing)

@main.route('/listing/<int:listing_id>/mark_sold')
@login_required
def mark_sold(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.user_id != current_user.id:
        flash('You can only mark your own listings as sold.')
        return redirect(url_for('main.view_listing', listing_id=listing_id))

    listing.status = 'sold'
    db.session.commit()
    flash('Your listing has been marked as sold!')
    return redirect(url_for('main.view_listing', listing_id=listing_id))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.enable_cross_platform_posting = 'enable_cross_platform' in request.form
        db.session.commit()
        flash('Your settings have been updated.')
        return redirect(url_for('main.profile'))

    listings = current_user.listings.order_by(Listing.id.desc()).all()
    notifications = current_user.notifications.order_by(Notification.timestamp.desc()).limit(10).all()
    return render_template('profile.html', user=current_user, listings=listings, notifications=notifications)

@main.route('/notifications')
@login_required
def notifications():
    notifications = current_user.notifications.order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@main.route('/notification/<int:notification_id>/mark_read')
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash('You can only mark your own notifications as read.')
        return redirect(url_for('main.notifications'))

    notification.is_read = True
    db.session.commit()
    flash('Notification marked as read.')
    return redirect(url_for('main.notifications'))
