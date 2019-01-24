from api.db.db_connect import Database
from api.views.routes import create_app
from api.models.user import User

app = create_app("development")

if __name__ == '__main__':
    app.run()