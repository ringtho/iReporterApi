from datetime import datetime
from api.resources.auth import admin_or_user
from api.resources.auth import check_user_id
from api.db.db_connect import Database

class RedFlag:

    """
    class for creating endpoints for a redflag record
    """
    
    def create_redflag(self,incident_type,location, created_by, images, videos,comment, status):
        cursor = Database().cursor
        create_redflag= """
        INSERT INTO redflags (incident_type, location, created_by, images, videos, comment, status) 
        VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(incident_type,location, created_by, images, videos,comment, status)
        return cursor.execute(create_redflag)
    
    def get_redflag_records(self,user_id):
        cursor = Database().cursor
        get_redflags = f"SELECT * FROM redflags WHERE created_by={user_id}"
        cursor.execute(get_redflags)
        redflags = cursor.fetchall()
        print(redflags)
        return redflags
    
    # def get_single_redflag(self):
    #     cursor = Database().cursor
        


    
