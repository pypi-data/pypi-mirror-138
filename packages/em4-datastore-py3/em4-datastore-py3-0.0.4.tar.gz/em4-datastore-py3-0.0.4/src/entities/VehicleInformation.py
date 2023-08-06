from google.cloud import ndb, datastore


class VehicleInformation(ndb.Model):
    user_id = ndb.IntegerProperty(required=True)
    client_id = ndb.IntegerProperty(required=True)
    ftp_id = ndb.IntegerProperty(required=True)
    tenant_id = ndb.IntegerProperty(required=True)
    imei = ndb.IntegerProperty(required=True)
    department = ndb.StringProperty()
    vin = ndb.StringProperty(required=True)
    license_plate = ndb.StringProperty(required=True)
    start_date = ndb.DateProperty()
    make = ndb.StringProperty()
    model = ndb.StringProperty()
    year = ndb.IntegerProperty()  # year is required
    vehicle_id = ndb.StringProperty()
    odometer = ndb.IntegerProperty()
    activity_date = ndb.DateProperty()
    software = ndb.JsonProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)
    ecm_expiry_date = ndb.DateProperty()
    latest_activity_date = ndb.DateTimeProperty()
    tested = ndb.BooleanProperty()
    comments = ndb.TextProperty()
