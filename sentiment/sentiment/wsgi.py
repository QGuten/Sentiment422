"""
WSGI config for sentiment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiment.settings')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentiment.pro_settings')     # 修改为复制新的settings文件名

application = get_wsgi_application()
