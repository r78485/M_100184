import os
from django.conf import settings

# Attempt to initialize Supabase client safely
try:
    from supabase import create_client, Client
    
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or getattr(settings, 'SUPABASE_URL', 'https://ivclauhftgpjghvqigaj.supabase.co')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or getattr(settings, 'SUPABASE_KEY', 'sb_publishable_UnTiIPs3X526ipGKjExIqA_zOxdkCI6')
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None
    print(f"Supabase Client Initialization Notice: {e}")

def get_supabase_client():
    """
    Returns the initialized Supabase client instance.
    """
    return supabase
