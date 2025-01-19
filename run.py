import os
from webapp import create_app

# Criando a aplicação Flask
app = create_app()

# A porta será configurada pelo Render
port = int(os.environ.get("PORT", 10000))
