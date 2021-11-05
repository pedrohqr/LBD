
import views
from flask import Flask

def create_app():
    """Factory principal de criação do App"""
    app = Flask(__name__)
    views.init_app(app)
    return app

if __name__ =='__main__':
    app = create_app()
    app.run('0.0.0.0', 4449)



