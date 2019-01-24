from api.db.db_connect import Database
from api.views.routes import app
from api.models.user import User



if __name__ == '__main__':
    app.run(debug=True)