import os
from flask import Flask



# create and configure app
def create_app(test_config=None):
    """indique à l'application que les
     fichiers de configuration sont relatifs au dossier
      d'instance"""
    app = Flask(__name__, instance_relative_config=True)

    """définit une configuration par 
    défaut que l'application utilisera:"""
    app.config.from_mapping(
        # est utilisé par Flask et les extensions pour protéger les données.
        SECRET_KEY='dev',
        # est le chemin où le fichier de base de données SQLite sera enregistré
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load   the instance config, if  it exist, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello babs tu es bien installer'

    # init-db a été enregistré avec l'application
    from . import db
    db.init_app(app)

    return app
