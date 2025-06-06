# Placeholder for app configuration

import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/data/lcca.db')

# Create data directory if it doesn't exist
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Database configuration options
DB_CONFIG = {
    'pool_size': 5,
    'max_overflow': 10,
    'pool_timeout': 30,
    'pool_recycle': 1800
}
