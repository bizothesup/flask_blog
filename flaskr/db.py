"""
current_app est un autre objet spécial qui pointe vers l'application Flask qui gère la demande.
"""
"""
g est un objet spécial unique pour chaque demande.
 Il est utilisé pour stocker des données auxquelles
 plusieurs fonctions pourraient accéder pendant la requête
"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# get_db() sera appelé lorsque l'application aura été créée et traitera une demande, donc current_app peut être utilisée
def get_db():
    if 'db' not in g:
        # sqlite3.connect()établit une connexion avec le fichier pointé par la DATABASEclé de configuration
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row indique à la connexion de renvoyer des lignes qui se comportent comme des repères.
        g.db.row_factory = sqlite3.Row
    return g.db


# close_db() vérifie si une connexion a été créée en vérifiant si g.db était défini.
#  Si la connexion existe, elle l'a  ferme.
def close_bd():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    #open_resource()ouvre un fichier relatif au flaskrpackage
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
#click.command()définit une commande de ligne de commande
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')