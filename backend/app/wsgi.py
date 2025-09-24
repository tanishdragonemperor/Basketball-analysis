"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()

# Auto-load sample data if database is empty
try:
    from app.dbmodels.models import Player
    
    # Check if we have any players in the database
    if Player.objects.count() == 0:
        logging.info("No players found in database. Loading sample data...")
        
        # Import and run the load_sample_data command
        from app.management.commands.load_sample_data import Command
        command = Command()
        command.handle()
        
        logging.info("Sample data loaded successfully!")
    else:
        logging.info(f"Database already has {Player.objects.count()} players. Skipping data load.")
        
except Exception as e:
    logging.error(f"Error loading sample data: {str(e)}")
    # Don't fail the application startup if data loading fails
