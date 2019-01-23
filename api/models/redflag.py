from datetime import datetime
from api.resources.auth import admin_or_user
from api.resources.auth import check_user_id
from api.db.db_connect import Database

cursor = Database().cursor


# count =0
class RedFlag:

    """
    class for creating endpoints for a redflag record
    """
    
    def create_redflag(self,incident_type,location, created_by, images, videos,comment, status):
        global cursor
        create_redflag= """
        INSERT INTO redflags (incident_type, location, created_by, images, videos, comment, status) 
        VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(incident_type,location, created_by, images, videos,comment, status)
        return cursor.execute(create_redflag)
    
    def get_redflag_records(self):
        global cursor
        get_redflags = "SELECT * FROM redflags"
        return cursor.execute(get_redflags)

# def get_red_flags_specific_user(redflags):
#     redflags_list = []
#     redflags_list = redflags
#     if not admin_or_user():
#         for redflag in redflags:
#             if redflag["createdBy"] == check_user_id():
#                 redflags_list.append(redflag)
        
#             return redflags
#     return redflag

    
