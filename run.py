import os
from webapp import create_app

app = create_app()

# Remova o if __name__ == '__main__': pois o Gunicorn não o usa
port = int(os.environ.get('PORT', 10000))