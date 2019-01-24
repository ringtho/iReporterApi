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

    def get_intervention_records(self,user_id):
        cursor = Database().cursor
        get_redflags = f"SELECT * FROM interventions WHERE created_by={user_id}"
        cursor.execute(get_redflags)
        interventions = cursor.fetchall()
        print(interventions)
        return interventions

    def get_single_intervention(self,intervention_id, user_id):
        cursor = Database().cursor
        query = f"SELECT * FROM interventions WHERE id={intervention_id} AND created_by={user_id}"
        cursor.execute(query)
        intervention = cursor.fetchone()
        return intervention

    def edit_location(self, intervention_id,location,user_id):
        cursor = Database().cursor
        query = f"UPDATE interventions SET location='{location}' WHERE id={intervention_id} AND created_by={user_id}"
        cursor.execute(query)
        return True