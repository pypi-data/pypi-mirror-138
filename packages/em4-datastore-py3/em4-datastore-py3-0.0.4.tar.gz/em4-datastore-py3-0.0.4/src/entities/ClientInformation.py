from google.cloud import ndb, datastore


class ClientInformation(ndb.Model):
    name = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    address1 = ndb.StringProperty()
    address2 = ndb.StringProperty()
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    zipcode = ndb.StringProperty()
