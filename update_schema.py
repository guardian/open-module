import logging
import models

from google.appengine.ext import deferred
from google.appengine.ext import ndb

BATCH_SIZE = 100

def UpdateSchema(cursor=None, num_updated=0):
    query = models.Snippet.query()

    logging.info("+++ HELLO")

    to_put = []
    res, cursor, more = query.fetch_page(BATCH_SIZE, start_cursor=cursor)


    for snippet in res:
         snippet.label = 'Share your stories'
         snippet.button_text = 'Tell us your story...'
         to_put.append(snippet)

    if to_put:
        ndb.put_multi(to_put)
        num_updated += len(to_put)
        logging.info(
           'Put %d entitities to Datastore for a total of %d',
           len(to_put), num_updated
        )

    if more:
        deferred.defer(UpdateSchema, cursor=cursor, num_updated=num_updated)
    else:
        logging.info('Update schema complete with %d updates!', num_updated)


