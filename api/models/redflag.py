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
    
    def get_single_redflag(self,redflag_id, user_id):
        cursor = Database().cursor
        get_redflag = f"SELECT * FROM redflags WHERE id={redflag_id} AND created_by={user_id}"
        cursor.execute(get_redflag)
        redflag = cursor.fetchone()
        return redflag
    
    def edit_location(self, redflag_id,location,user_id):
        cursor = Database().cursor
        query = f"UPDATE redflags SET location='{location}' WHERE id={redflag_id} AND created_by={user_id}"
        cursor.execute(query)
        return True
       

    def edit_comment(self, redflag_id,comment,user_id):
        cursor = Database().cursor
        query = f"UPDATE redflags SET comment='{comment}' WHERE id={redflag_id} AND created_by={user_id}"
        cursor.execute(query)
        return True
    
    def delete_redflag_record(self,redflag_id,user_id):
        cursor = Database().cursor
        query = f"DELETE FROM redflags WHERE id={redflag_id} AND created_by={user_id}"
        cursor.execute(query)
        rows = cursor.rowcount
        return rows

    # def edit_status_admin(self, redflag_id,status):
    #     cursor = Database().cursor
    #     query = f"UPDATE redflags SET status='{status}' WHERE id={redflag_id}"
    #     cursor.execute(query)
    #     rows = cursor.rowcount
    #     return rows


        


    
