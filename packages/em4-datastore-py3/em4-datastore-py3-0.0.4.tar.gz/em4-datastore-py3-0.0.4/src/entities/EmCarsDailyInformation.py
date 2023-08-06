from google.cloud import ndb, datastore


class EmCarsDailyInformation(ndb.Model):
    date = ndb.DateProperty()
    time = ndb.TimeProperty()
    ftp_id = ndb.IntegerProperty(required=True)
    data_type = ndb.BooleanProperty(required=True)
    pid_data = ndb.PickleProperty()
    vin = ndb.StringProperty()
