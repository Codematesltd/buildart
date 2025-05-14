from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from supabase import create_client
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import io

# Setup
admin_bp = Blueprint('admin', __name__)

# Initialize Supabase
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class CSRFForm(FlaskForm):
    pass

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class Admin:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            response = supabase.table('admin_users').select('*').eq('username', form.username.data).execute()
            if response.data and response.data[0]['password_hash'] == form.password.data:
                user_data = response.data[0]
                user = Admin(user_data['id'], user_data['username'])
                login_user(user)
                return redirect(url_for('admin.dashboard'))
            flash('Invalid username or password', 'error')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'error')
    return render_template('admin_login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

def get_supabase():
    """Get Supabase client from app config"""
    return current_app.config['supabase']

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    section = request.args.get('section', 'applications')  # Default to applications view
    queries = []
    careers = []
    
    try:
        supabase = current_app.config['supabase']
        
        # Always fetch both queries and careers
        queries_response = supabase.table('general_inquiries').select('*').execute()
        careers_response = supabase.table('careers').select('*').execute()
        
        queries = queries_response.data if queries_response.data else []
        careers = careers_response.data if careers_response.data else []
        
        print(f"Fetched {len(careers)} career applications")  # Debug print
        
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
    
    return render_template(
        'admin_dashboard.html',
        section=section,
        queries=queries,
        careers=careers
    )

@admin_bp.route('/update_query_status', methods=['POST'])
@login_required
def update_query_status():
    try:
        data = request.get_json()
        query_id = data.get('query_id')
        new_status = data.get('status')
        
        if not query_id or not new_status:
            return jsonify({'success': False, 'error': 'Missing required data'})
        
        # Update the status in Supabase
        supabase = current_app.config['supabase']
        response = supabase.table('general_inquiries').update(
            {'status': new_status}
        ).eq('id', query_id).execute()
        
        if response.data:
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to update status'})
        
    except Exception as e:
        print(f"Error updating status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/update_career_status', methods=['POST'])
@login_required
def update_career_status():
    try:
        data = request.get_json()
        career_id = data.get('career_id')
        new_status = data.get('status')
        
        if not career_id or not new_status:
            return jsonify({'success': False, 'error': 'Missing data'})
            
        supabase = current_app.config['supabase']
        response = supabase.table('careers').update(
            {'status': new_status}
        ).eq('id', career_id).execute()
        
        return jsonify({'success': True if response.data else False})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/add_award', methods=['POST'])
@login_required
def add_award():
    if request.method == 'POST':
        award_data = {
            'year': request.form.get('year'),
            'award_name': request.form.get('award_name'),
            'project': request.form.get('project_name'),
            'category': request.form.get('category'),  # Add this line
            'prize': request.form.get('prize')
        }
        response = supabase.table('awards').insert(award_data).execute()
        if response.data:
            flash('Award added successfully!', 'success')
        return redirect(url_for('main.awards'))

@admin_bp.route('/manage/awards', methods=['POST'])
@login_required
def manage_awards():
    if request.method == 'POST':
        supabase = get_supabase()
        
        # Create new award
        award_data = {
            'id': str(uuid.uuid4()),
            'year': request.form.get('year'),
            'award_name': request.form.get('award_name'),
            'project': request.form.get('project'),
            'category': request.form.get('category'),
            'prize': request.form.get('prize'),
            'images': []  # We'll handle image upload separately
        }
        
        # Handle image uploads
        if 'images[]' in request.files:
            images = request.files.getlist('images[]')
            for image in images:
                if image.filename:
                    # Handle image upload to Supabase storage
                    filename = secure_filename(image.filename)
                    file_path = f"awards/{award_data['id']}/{filename}"
                    
                    # Upload to Supabase storage
                    supabase.storage.from_('award-images').upload(file_path, image)
                    
                    # Add image URL to award data
                    award_data['images'].append(file_path)
        
        # Insert into Supabase
        response = supabase.table('awards').insert(award_data).execute()
        
        if response.data:
            flash('Award added successfully!', 'success')
        else:
            flash('Error adding award', 'error')
            
        return redirect(url_for('admin.dashboard', section='awards'))
