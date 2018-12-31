from datetime import datetime
from random import randint

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
