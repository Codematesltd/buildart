from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import login_manager

admin_bp = Blueprint('admin', __name__)

class Admin:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    # This is a simple example. In production, you should implement proper user storage
    if username == "admin":
        return Admin(username)
    return None

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # In production, implement proper authentication
        if username == "admin" and password == "admin":
            user = Admin(username)
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials')
    return render_template('admin_login.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))