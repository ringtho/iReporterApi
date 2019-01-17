from datetime import datetime
from api.resources.auth import admin_or_user
from api.resources.auth import check_user_id


count =0
class RedFlag:

    """
    class for creating endpoints for a redflag record
    """
    
    def __init__(self,**kwargs):
        global count
        count+=1
        self.id = count
        self.createdOn = datetime.today()
        self.createdBy = kwargs['createdBy']
        self.types = kwargs['types']
        self.location = kwargs['location']
        self.status = kwargs['status']
        self.images = kwargs['images']
        self.videos = kwargs['videos']
        self.comment = kwargs['comment']

        

    def json_format(self):
        format = {
        "id": self.id,
        "createdOn": self.createdOn,
        "createdBy":self.createdBy,
        "types": self.types,
        "location": self.location,
        "status": self.status,
        "images": self.images,
        "videos": self.videos,
        "comment": self.comment
        }
        return format

# def get_red_flags_specific_user(redflags):
#     redflags_list = []
#     redflags_list = redflags
#     if not admin_or_user():
#         for redflag in redflags:
#             if redflag["createdBy"] == check_user_id():
#                 redflags_list.append(redflag)
        
#             return redflags
#     return redflag

    
