from src.app import create_app
from flask.cli import with_appcontext
import click
from src.app.db import populate_db
# from src.app.routes import routes


app = create_app()
# routes(app)

@click.command(name = 'populate_db')
@with_appcontext
def call_command():
  populate_db()

app.cli.add_command(call_command)

if __name__ == "__main__":
  app.run()