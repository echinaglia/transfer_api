from flask import request, abort
from flask_restplus import Resource, Namespace
from marshmallow import ValidationError

from api import factory
from api.database.mongodb import insert, find_one
from api.schemas.transfer import TransferSchemaLoad, TransferSchemaDump, IdSchema, StatusSchema
from api.tasks.transfer import transfer_request

api = Namespace(name='')
celery = factory.celery


@api.route('/fund-transfer/<string:transaction_id>')
class Status(Resource):
    def get(self, transaction_id):
        if not transaction_id:
            abort(400, 'You need to pass some transaction id like /api/fund-transfer/{{transactionId}}')

        status = find_one({'_id': transaction_id})
        if not status:
            abort(404, 'Transaction ID not found')

        return StatusSchema().dump(status)


@api.route('/fund-transfer/')
class Transfer(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            abort(400, 'You need to send the transfer data')
        try:
            transfer = TransferSchemaLoad().load(data)
        except ValidationError as e:
            abort(400, e.messages)

        transfer = TransferSchemaDump().dump(transfer)
        transfer_id = insert(transfer)
        transfer_request.apply_async((transfer_id,))
        return IdSchema().dump(transfer)
