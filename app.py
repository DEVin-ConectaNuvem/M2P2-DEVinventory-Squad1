from src.app import create_app
from src.app.routes import routes

app = create_app()
routes(app)

if __name__ == "__main__":
  app.run()