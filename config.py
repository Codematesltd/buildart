import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or 'https://zpnparyxnrtfbxnwriyv.supabase.co'
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwbnBhcnl4bnJ0ZmJ4bndyaXl2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY3OTAxMTcsImV4cCI6MjA2MjM2NjExN30.mg_g4fw-AiabzKUJnWxU7C10eiCUCQAurygIv5fzWG0'