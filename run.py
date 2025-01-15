import os
from webapp import create_app

app = create_app()

port = int(os.environ.get('PORT', 10000))