from google.cloud import ndb, datastore

class InsuranceInformation(ndb.Model):
    client_id = ndb.IntegerProperty(required=True)
    insurance_company = ndb.StringProperty()
    naic = ndb.StringProperty()
    policy = ndb.StringProperty()
    expiry = ndb.DateTimeProperty()