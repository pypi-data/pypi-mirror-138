Installing

pip install em4-datastore-py3

Usage

>>> from src.methods import Em4DataStore
>>> db = Em4DataStore()
>>> message, client_id = ds.upsertClient(name=client_name,
                                         lastname=lastname,
                                         phone=phone,
                                         email=email,
                                         address1=address1,
                                         address2=address2,
                                         city=city,
                                         state=state,
                                         zipcode=zipcode)
