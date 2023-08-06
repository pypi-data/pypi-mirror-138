from google.cloud import ndb, datastore


class AdminAuthInformation(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
