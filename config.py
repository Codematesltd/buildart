import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or 'https://zpnparyxnrtfbxnwriyv.supabase.co'
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwbnBhcnl4bnJ0ZmJ4bndyaXl2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY3OTAxMTcsImV4cCI6MjA2MjM2NjExN30.mg_g4fw-AiabzKUJnWxU7C10eiCUCQAurygIv5fzWG0'
    
    # Security Configurations
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_SSL_STRICT = True
    
    # Content Security Policy
    TALISMAN_CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'img-src': "'self' data:",
        'script-src': "'self'",
        'style-src': "'self' 'unsafe-inline'"
    }
    TALISMAN_FORCE_HTTPS = True
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"

    # Cache Configuration
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes in seconds