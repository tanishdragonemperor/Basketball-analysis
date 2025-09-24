#!/usr/bin/env python3
"""
Simple script to populate the database with sample data
Run this script on Railway to load the basketball data
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Import the management command
from app.management.commands.load_sample_data import Command

if __name__ == '__main__':
    print("Starting database population...")
    command = Command()
    command.handle()
    print("Database population completed!")
