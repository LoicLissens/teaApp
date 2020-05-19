from app import app, db
# Importing db Model and set up things to work with  flas shell
from app.models import User, Tea, Region
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Tea': Tea, 'Region': Region}
