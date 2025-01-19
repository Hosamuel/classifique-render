import os
from webapp import create_app

# Criando a aplicação Flask
app = create_app()

# A porta será configurada pelo Render
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

