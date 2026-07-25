"""
Django settings for school_management project.
"""
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-replace-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.up.railway.app', 'https://*.onrender.com', 'https://m-100184.onrender.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'apps.users',
    'apps.academics',
    'apps.attendance',
    'apps.transcripts',
    'apps.admit_cards',
    'apps.testimonials',
    'apps.sync',  # অফলাইন-অনলাইন সিঙ্ক সিস্টেম
    'apps.question_paper',
]

MIDDLEWARE = [
    'school_management.middleware.AutoMigrateMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'school_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Root templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'school_management.wsgi.application'

# Database Setup (Supports PostgreSQL on Railway and fallback to SQLite locally)
try:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
            conn_max_age=600
        )
    }
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Auth redirect settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('bn', 'Bengali'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static & Media files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────────────────────
# অফলাইন ↔ অনলাইন সিঙ্ক কনফিগারেশন
# ──────────────────────────────────────────────────────────────
# অনলাইন সার্ভারের URL (নেটওয়ার্ক ব্যাকআপ)
ONLINE_SERVER_URL = os.environ.get('ONLINE_SERVER_URL', 'https://m-100184.onrender.com')

# সিঙ্ক API কী — উভয় সার্ভারে একই কী থাকতে হবে
# প্রোডাকশনে অবশ্যই env variable দিয়ে বদলান!
SYNC_API_KEY = os.environ.get('SYNC_API_KEY', 'offline-sync-secret-key-change-me')

# স্বয়ংক্রিয় সিঙ্কের বিরতি (সেকেন্ড) — ডিফল্ট ১৫ মিনিট
SYNC_INTERVAL_SECONDS = int(os.environ.get('SYNC_INTERVAL_SECONDS', 900))

# Auto-compile translations on reload
try:
    import struct
    _LOCALE_DIR = os.path.join(BASE_DIR, 'locale', 'bn', 'LC_MESSAGES')
    os.makedirs(_LOCALE_DIR, exist_ok=True)
    _PO_FILE = os.path.join(_LOCALE_DIR, 'django.po')
    _MO_FILE = os.path.join(_LOCALE_DIR, 'django.mo')
    
    from .translations import _translations
    
    _po_content = 'msgid ""\nmsgstr ""\n"Project-Id-Version: EduManage ERP\n"\n"Report-Msgid-Bugs-To: \n"\n"POT-Creation-Date: 2026-07-20 00:00+0000\n"\n"PO-Revision-Date: 2026-07-20 00:00+0000\n"\n"Language: bn\n"\n"MIME-Version: 1.0\n"\n"Content-Type: text/plain; charset=UTF-8\n"\n"Content-Transfer-Encoding: 8bit\n"\n\n'
    for eng, bn in _translations.items():
        _po_content += f'msgid "{eng}"\nmsgstr "{bn}"\n\n'
        
    with open(_PO_FILE, 'w', encoding='utf-8') as f:
        f.write(_po_content)
        
    def _generate_mo(po_dict, output_path):
        keys = sorted(po_dict.keys())
        offsets = []
        ids = b''
        strs = b''
        for k in keys:
            v = po_dict[k]
            k_enc = k.encode('utf-8')
            v_enc = v.encode('utf-8')
            offsets.append((len(k_enc), len(ids), len(v_enc), len(strs)))
            ids += k_enc + b'\0'
            strs += v_enc + b'\0'
        output = bytearray()
        output.extend(struct.pack('<I', 0x950412de))
        output.extend(struct.pack('<I', 0))
        output.extend(struct.pack('<I', len(keys)))
        orig_table_offset = 28
        trans_table_offset = 28 + 8 * len(keys)
        hash_table_size = 0
        hash_table_offset = 28 + 16 * len(keys)
        output.extend(struct.pack('<I', orig_table_offset))
        output.extend(struct.pack('<I', trans_table_offset))
        output.extend(struct.pack('<I', hash_table_size))
        output.extend(struct.pack('<I', hash_table_offset))
        for length, offset, _, _ in offsets:
            output.extend(struct.pack('<I', length))
            output.extend(struct.pack('<I', orig_table_offset + 8 * len(keys) * 2 + offset))
        for _, _, length, offset in offsets:
            output.extend(struct.pack('<I', length))
            output.extend(struct.pack('<I', orig_table_offset + 8 * len(keys) * 2 + len(ids) + offset))
        output.extend(ids)
        output.extend(strs)
        with open(output_path, 'wb') as f:
            f.write(output)
            
    _mo_dict = {"": "Project-Id-Version: EduManage ERP\nReport-Msgid-Bugs-To: \nPOT-Creation-Date: 2026-07-20 00:00+0000\nPO-Revision-Date: 2026-07-20 00:00+0000\nLanguage: bn\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n"}
    for eng, bn in _translations.items():
        _mo_dict[eng] = bn
        
    _generate_mo(_mo_dict, _MO_FILE)
except Exception as e:
    pass
