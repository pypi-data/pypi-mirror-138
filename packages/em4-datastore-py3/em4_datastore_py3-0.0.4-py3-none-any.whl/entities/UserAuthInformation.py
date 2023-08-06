from google.cloud import ndb, datastore


class UserAuthInformation(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty()
    password_reset = ndb.BooleanProperty()
    client_id = ndb.IntegerProperty(required=True)
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    admin = ndb.BooleanProperty(default=False)
