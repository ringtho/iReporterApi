from api.db.db_connect import Database
from api.views.routes import app

app.config.from_object("config.Development")
if __name__ == '__main__':

    app.run()