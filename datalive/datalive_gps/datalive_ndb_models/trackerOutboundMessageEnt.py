from google.appengine.ext import ndb

class TrackerOutboundMessage(ndb.Model):
    action = ndb.IntegerProperty() # for now these just match the Calamp Unit Request Message actions, 3  = PEG action
    state = ndb.IntegerProperty() # 0 = active, 1 = delivered, 2 = read, 3 = cancelled, 4 = timedout
    userKey = ndb.KeyProperty() # user that created this
    intParameterList = ndb.IntegerProperty(repeated = True)
    stringParameterList = ndb.StringProperty(repeated = True)
    creationDateTime = ndb.DateTimeProperty(auto_now_add=True)
    timeoutDateTime = ndb.DateTimeProperty()

