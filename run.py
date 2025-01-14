import sys
from pathlib import Path

# Adiciona o diretório correto ao sys.path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from webapp import create_app  

app = create_app()

if __name__ == '__main__':
    # Em produção, estas configurações serão ignoradas pois usaremos o gunicorn
    app.run(host='0.0.0.0', port=10000)