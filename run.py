import os
from webapp import create_app

# Criando a aplicação Flask
app = create_app()

if __name__ == "__main__":
    # Porta definida pelo ambiente ou padrão 10000
    port = int(os.environ.get('PORT', 10000))
    # Inicia o servidor Flask, ouvindo em todas as interfaces de rede
    app.run(host="0.0.0.0", port=port)
