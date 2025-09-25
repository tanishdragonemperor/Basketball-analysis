
import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()

try:
    from app.dbmodels.models import Player
    
    if Player.objects.count() == 0:
        logging.info("No players found in database. Loading sample data...")
        
        from app.management.commands.load_sample_data import Command
        command = Command()
        command.handle()
        
        logging.info("Sample data loaded successfully!")
    else:
        logging.info(f"Database already has {Player.objects.count()} players. Skipping data load.")
        
except Exception as e:
    logging.error(f"Error loading sample data: {str(e)}")
