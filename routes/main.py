from flask import Blueprint, render_template, request, flash, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime
from routes.admin import supabase

load_dotenv()

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/projects')
def projects():
    return render_template('projects.html')

@main_bp.route('/awards')
def awards():
    return render_template('awards.html')

@main_bp.route('/careers', methods=['GET', 'POST'])
def careers():
    if request.method == 'POST':
        try:
            # Initialize Supabase client
            supabase = create_client(
                os.getenv('SUPABASE_URL'),
                os.getenv('SUPABASE_KEY')
            )

            # Insert data into careers table
            data = supabase.table('careers').insert({
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'position': request.form.get('position'),
                'message': request.form.get('message')
            }).execute()

            flash('Your application has been submitted successfully! We will get back to you soon.', 'success')
            return redirect(url_for('main.careers'))

        except Exception as e:
            print(f"Error: {str(e)}")
            flash('There was an error submitting your application. Please try again.', 'error')
            
    return render_template('careers.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            # Initialize Supabase client
            supabase: Client = create_client(
                os.getenv('SUPABASE_URL'),
                os.getenv('SUPABASE_KEY')
            )

            # Insert data into general_inquiries table
            data = supabase.table('general_inquiries').insert({
                "name": name,
                "email": email,
                "message": message
            }).execute()

            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))

        except Exception as e:
            print(f"Error: {str(e)}")
            flash('An error occurred while sending your message. Please try again.', 'error')
            
    return render_template('contact.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Your login logic here
            return redirect(url_for('main.index'))
    return render_template('login.html', form=form)
