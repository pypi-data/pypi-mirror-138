from google.cloud import ndb, datastore


class LastRunDate(ndb.Model):
    process_id = ndb.StringProperty(required=True)
    last_run_date = ndb.DateProperty(required=True)
