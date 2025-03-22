from flask import Flask
from webapp.routes import main

app = Flask(__name__, 
    template_folder='webapp/templates',  
    static_folder='webapp/static'        
)

# Blueprint
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
