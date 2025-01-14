import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

from webapp import create_app  

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)