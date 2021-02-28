from api import factory
from api.database.mongodb import find_one, update_one
from api.services.account_api import get_account, post_transfer

celery = factory.celery


@celery.task()
def transfer_request(transfer_id):
    _filter = {'_id': transfer_id}
    update_one(_filter, {'$set': {'status': 'processing'}})

    transfer = find_one(_filter, 'transfer')

    origin, err = get_account(transfer['accountOrigin'])
    if err:
        update_one(_filter, {'$set': {'status': 'error', 'message': err}})
        return

    destination, err = get_account(transfer['accountDestination'], origin=False)
    if err:
        update_one(_filter, {'$set': {'status': 'error', 'message': err}})
        return

    if transfer['value'] > origin['balance']:
        update_one(_filter, {'$set': {'status': 'error', 'message': 'Account without balance'}})
        return

    err = post_transfer(transfer)
    if err:
        update_one(_filter, {'$set': {'status': 'error', 'message': err}})
        return

    update_one(_filter, {'$set': {'status': 'confirmed'}})
