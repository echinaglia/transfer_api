import uuid

from pymongo.helpers import DuplicateKeyError

from api import factory


def insert(data, collection='transfer'):
    col = factory.db[collection]
    try:
        col.insert_one(data)
    except DuplicateKeyError:
        data['_id'] = str(uuid.uuid4())
        col.insert_one(data)

    return data['_id']


def find_one(_filter, collection='transfer'):
    col = factory.db[collection]

    return col.find_one(_filter)


def update_one(_filter, data, collection='transfer'):
    col = factory.db[collection]
    col.update_one(_filter, data)
