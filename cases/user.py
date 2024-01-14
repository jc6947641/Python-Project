from flask import render_template,jsonify,request,url_for,redirect,session,flash
from models import User,db

def go_user(app):

    @app.route('/user')
    def user():
        # Fetch all cargo records from the database
        user_id = session.get('user_id')
        print(user_id)
        user_list = User.query.filter_by(id=user_id).all()

        return render_template('user.html', user_list=user_list)

    @app.route('/alter_user', methods=['GET', 'POST'])
    def alter_user():
        user_id = session.get('user_id')
        print(user_id)
        if request.method == 'POST':
            # Get data from the form
            name = request.form.get('name')
            address = request.form.get('address')
            tel = request.form.get('tel')  # Keep as string to preserve leading zeros

            # Retrieve and update user information
            user = User.query.filter_by(id=user_id).first()
            if user:
                user.name = name
                user.address = address
                user.tel = tel
                db.session.commit()
                # Add a message about successful update
                flash('User information updated successfully.')
            else:
                # Handle case where user is not found
                flash('User not found.')

            return redirect(url_for('homelist'))

        return render_template('alter_user.html')