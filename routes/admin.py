from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from supabase import create_client
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

# Setup
admin_bp = Blueprint('admin', __name__)
login_manager = LoginManager()
login_manager.login_view = 'admin.login'

# Initialize Supabase
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class CSRFForm(FlaskForm):
    pass

class Admin:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

def init_extensions(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    response = supabase.table('admin_users').select('*').eq('id', user_id).execute()
    if response.data:
        user_data = response.data[0]
        return Admin(user_data['id'], user_data['username'])
    return None

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        response = supabase.table('admin_users').select('*').eq('username', form.username.data).execute()
        if response.data and response.data[0]['password_hash'] == form.password.data:
            user_data = response.data[0]
            user = Admin(user_data['id'], user_data['username'])
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials')
    return render_template('admin_login.html', form=form)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    form = CSRFForm()
    # Get existing projects and awards
    projects = supabase.table('projects').select('*').execute()
    awards = supabase.table('awards').select('*').execute()
    return render_template('admin_dashboard.html', 
                         form=form, 
                         projects=projects.data if projects.data else [],
                         awards=awards.data if awards.data else [])

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

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

@admin_bp.route('/projects', methods=['GET', 'POST'])
@login_required
def manage_projects():
    if request.method == 'POST':
        try:
            files = request.files.getlist('images[]')
            image_urls = []
            
            if not files or files[0].filename == '':
                flash('No files selected', 'error')
                return redirect(url_for('admin.dashboard'))

            for file in files:
                if file and allowed_file(file.filename):
                    try:
                        filename = f"projects/{uuid.uuid4()}_{secure_filename(file.filename)}"
                        file_content = file.read()
                        
                        storage_response = supabase.storage \
                            .from_('project-images') \
                            .upload(filename, file_content)
                        
                        if hasattr(storage_response, 'path'):
                            bucket_url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/project-images"
                            public_url = f"{bucket_url}/{storage_response.path}"
                            image_urls.append(public_url)
                            print(f"Image URL added: {public_url}")
                        else:
                            print(f"Upload failed, unexpected response: {storage_response}")
                            
                    except Exception as e:
                        print(f"File upload error: {str(e)}")
                        continue

            # Simplified project data without thumbnail_url
            project_data = {
                'name': request.form.get('name'),
                'description': request.form.get('description'),
                'image_urls': image_urls,
                'created_at': datetime.utcnow().isoformat()
            }
            
            print("Project data being inserted:", project_data)
            
            response = supabase.table('projects').insert(project_data).execute()
            if hasattr(response, 'data'):
                flash('Project added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
            
        except Exception as e:
            print(f"Error: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('admin.dashboard'))

    # GET request handling remains the same
    return render_template('admin_dashboard.html')

@admin_bp.route('/awards', methods=['GET', 'POST'])
@login_required
def manage_awards():
    if request.method == 'POST':
        try:
            files = request.files.getlist('images[]')
            image_urls = []
            
            if not files or files[0].filename == '':
                flash('No files selected', 'error')
                return redirect(url_for('admin.dashboard'))

            for file in files:
                if file and allowed_file(file.filename):
                    try:
                        filename = f"awards/{uuid.uuid4()}_{secure_filename(file.filename)}"
                        file_content = file.read()
                        
                        storage_response = supabase.storage \
                            .from_('project-images') \
                            .upload(filename, file_content)
                        
                        if hasattr(storage_response, 'path'):
                            bucket_url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/project-images"
                            public_url = f"{bucket_url}/{storage_response.path}"
                            image_urls.append(public_url)
                            print(f"Image URL added: {public_url}")
                        else:
                            print(f"Upload failed, unexpected response: {storage_response}")
                            
                    except Exception as e:
                        print(f"File upload error: {str(e)}")
                        continue

            award_data = {
                'year': request.form.get('year'),
                'award_name': request.form.get('award_name'),
                'project': request.form.get('project'),
                'category': request.form.get('category'),  # Add this line
                'prize': request.form.get('prize'),
                'image_urls': image_urls,  # This should now contain valid URLs
                'created_at': datetime.utcnow().isoformat()
            }

            print("Award data being inserted:", award_data)  # Debug log
            
            response = supabase.table('awards').insert(award_data).execute()
            if hasattr(response, 'data'):
                flash('Award added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))

        except Exception as e:
            print(f"Error: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('admin.dashboard'))

    # GET request handling remains the same
    return render_template('admin_dashboard.html')