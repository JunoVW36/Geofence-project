from google.appengine.ext import ndb

class VehicleMessage(ndb.Model):
    vehicleKey = ndb.KeyProperty() # vehicle this message was sent to
    customerKey = ndb.KeyProperty() # key to customer that owns the vehicle
    currentTracker = ndb.IntegerProperty() # tracker that was attached to vehicle at the time of sending
    creationDateTime = ndb.DateTimeProperty(auto_now_add=True)
    deliveredDateTime = ndb.DateTimeProperty()
    acceptedDateTime = ndb.DateTimeProperty()
    messageStatus = ndb.IntegerProperty() # 0=none, 1=queued to send, 2=sent waiting driver accept, 3=accepted, 4=timedout
    
    #@classmethod
    #def query_vehicleMessage(cls, reg):
    #    return cls.query(VehicleMessage.registration==reg).order(-cls.creationDateTime)
    
    @classmethod
    def get_all(cls):
        return cls.query().order(-cls.creationDateTime)
