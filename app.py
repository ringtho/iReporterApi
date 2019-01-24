from api.db.db_connect import Database
from api.views.routes import app
from api.models.user import User

db = Database()
# user_obj = User()

if __name__ == '__main__':
    # user_obj.create_admin()
    app.run(debug=True)