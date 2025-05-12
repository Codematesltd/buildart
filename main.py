from flask import Blueprint, render_template, request, flash, redirect, url_for
from supabase import create_client
import os
import time
from dotenv import load_dotenv

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Add small delay to show loading state
            time.sleep(1)
            
            supabase = create_client(
                os.getenv('SUPABASE_URL'),
                os.getenv('SUPABASE_KEY')
            )

            data = supabase.table('general_inquiries').insert({
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'message': request.form.get('message')
            }).execute()

            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            print(f"Error: {str(e)}")
            flash('An error occurred. Please try again later.', 'error')
            
    return render_template('contact.html')
