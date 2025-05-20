from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from flask_mail import Mail, Message

main_bp = Blueprint('main', __name__)
mail = Mail()

def get_supabase():
    """Get Supabase client from app config"""
    from flask import current_app
    return current_app.config['supabase']

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/projects')
def projects():
    supabase = current_app.config['supabase']
    try:
        # Fetch projects from Supabase
        response = supabase.table('projects').select('*').execute()
        projects = response.data if response.data else []

        # Transform image URLs for each project
        for project in projects:
            project['image_urls'] = []
            if project.get('images'):
                # Convert string to list if needed
                images = project['images']
                if isinstance(images, str):
                    import json
                    images = json.loads(images)
                    
                # Get full URLs for each image
                project['image_urls'] = [
                    supabase.storage.from_('project-images').get_public_url(img)
                    for img in images
                ]

        return render_template('projects.html', supabase_projects=projects)
    except Exception as e:
        print(f"Error fetching projects: {str(e)}")
        return render_template('projects.html', supabase_projects=[])

@main_bp.route('/awards')
def awards():
    try:
        # Fetch awards from Supabase
        supabase = current_app.config['supabase']
        response = supabase.table('awards').select('*').order('year', desc=True).execute()
        db_awards = response.data if response.data else []
    except Exception as e:
        print(f"Error fetching awards: {str(e)}")
        db_awards = []
    
    return render_template('awards.html', db_awards=db_awards)

@main_bp.route('/careers', methods=['GET', 'POST'])
def careers():
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'position': request.form.get('position'),
                'message': request.form.get('message'),
                'status': 'pending'
            }
            
            # Save to Supabase
            supabase = current_app.config['supabase']
            response = supabase.table('careers').insert(data).execute()
            
            if response.data:
                flash('Your application has been submitted successfully!', 'success')
            else:
                flash('There was an error submitting your application. Please try again.', 'error')
            return redirect(url_for('main.careers'))
            
        except Exception as e:
            print(f"Error submitting application: {str(e)}")
            flash('There was an error submitting your application. Please try again.', 'error')
            return redirect(url_for('main.careers'))
    
    return render_template('careers.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Check if form was already submitted
        form_token = request.form.get('form_token')
        if not form_token or form_token != session.get('form_token'):
            flash('Form already submitted or invalid submission.', 'error')
            return redirect(url_for('main.contact'))
            
        try:
            # Clear the form token to prevent resubmission
            session.pop('form_token', None)
            
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Validate required fields
            if not all([name, email, message]):
                flash('All fields are required', 'error')
                return redirect(url_for('main.contact'))
            
            # Check for duplicate submission
            supabase = current_app.config['supabase']
            check_duplicate = supabase.table('general_inquiries').select('*')\
                .eq('email', email)\
                .eq('message', message)\
                .execute()
                
            if check_duplicate.data:
                flash('A similar message has already been submitted.', 'warning')
                return redirect(url_for('main.contact'))
            
            # If no duplicate, proceed with insertion
            data = {
                'name': name,
                'email': email,
                'message': message
                # status and created_at will use table defaults
            }
            
            response = supabase.table('general_inquiries').insert(data).execute()
            
            if response.data:
                flash('Thank you for your message! We will get back to you soon.', 'success')
            else:
                flash('There was an error sending your message. Please try again.', 'error')
                
            return redirect(url_for('main.contact'))
            
        except Exception as e:
            print(f"Error saving contact form: {str(e)}")
            flash('An unexpected error occurred. Please try again later.', 'error')
            return redirect(url_for('main.contact'))
    else:
        # Generate new token for GET request
        import secrets
        session['form_token'] = secrets.token_hex(16)
    
    return render_template('contact.html')
