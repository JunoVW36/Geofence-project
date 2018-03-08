from google.appengine.ext import ndb

class trackerPoint(ndb.Expando):
    updateDateTime = ndb.DateTimeProperty()
    lat = ndb.IntegerProperty()
    lon = ndb.IntegerProperty()
    altitude = ndb.IntegerProperty()
    speed = ndb.IntegerProperty()
    heading = ndb.IntegerProperty()
    eventCode = ndb.IntegerProperty()
    #accum0 = ndb.IntegerProperty()  # may not exist
    #accum1 = ndb.IntegerProperty()
    
    @classmethod
    def query_trackerPoint(cls, ancestor_key):
        return cls.query(ancestor = ancestor_key).order(-cls.updateDateTime)
    
    @classmethod
    def query_tracePoints(cls, ancestor_key, start_datetime, end_datetime):
        #return cls.query(ancestor = ancestor_key).add_filter('updateDateTime', '>=', start_datetime).add_fileter('updateDateTime', '<=', end_datetime).order(-cls.updateDateTime)
        # Could we order by key and save some writes?
        return cls.query(cls.updateDateTime >= start_datetime, cls.updateDateTime <= end_datetime, ancestor = ancestor_key).order(cls.updateDateTime)
        #return cls.query(ancestor = ancestor_key).order(-cls.updateDateTime)

    def getODO(self):
        #print (self)
        try:
            if self.accum0 != 0:
                return self.accum0  # VBUS/CAN ODO
            else:
                return self.accum1  # GPS ODO
        except Exception as e:  # Exception accum0 or accum1 don't exist
            print e
            return 0 


    def getIdleDurationSeconds(self):
        try:
            if hasattr(point, 'accum11'):  # on units not returning accum11 then accum3 has a different meaning
                return self.accum3  # Idle duration, reset at every key on
            else:
                return 0
        except Exception as e:  # Exception accum3 doesn't exist
            return 0


    def getSpeedingDistance(self):
        try:
            return self.accum11  # Speeding distance, reset at every key on
        except Exception as e:  # Exception accum11 doesn't exist
            return 0
