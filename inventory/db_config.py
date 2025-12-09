"""
Database connection configuration for the Hotel Management System.
Include this in your Django project's settings.py.
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hotel_system',
        'USER': 'root',       # specific to User's environment (likely root/empty or standard)
        'PASSWORD': '',       # specific to User's environment
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Ensure you have 'mysqlclient' or 'pymysql' installed.
# pip install mysqlclient
