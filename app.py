from api.db.db_connect import Database
from api.views.routes import app


if __name__ == '__main__':

    app.run(debug=True)