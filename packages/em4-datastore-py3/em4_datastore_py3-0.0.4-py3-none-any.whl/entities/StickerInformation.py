from google.cloud import ndb, datastore


class StickerInformation(ndb.Model):
    ftp_id = ndb.IntegerProperty(required=True)
    client_id = ndb.IntegerProperty()
    sticker = ndb.StringProperty()
    expiry = ndb.DateTimeProperty()
