from api.resources.auth import admin_or_user
from api.resources.auth import check_user_id
from api.db.db_connect import Database

class Intervention:

    """
    class for creating endpoints for an intervention record
    """
    
    def create_intervention(self,incident_type,location, created_by, images, videos,comment, status):
        cursor = Database().cursor
        create_intervention= """
        INSERT INTO interventions (incident_type, location, created_by, images, videos, comment, status) 
        VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(incident_type,location, created_by, images, videos,comment, status)
        return cursor.execute(create_intervention)