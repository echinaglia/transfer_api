import uuid

from marshmallow import Schema, fields, validate


class TransferSchemaLoad(Schema):
    accountOrigin = fields.String(required=True, nullable=False,
                                  validate=[validate.NoneOf([''], error='Field may not be null.')])
    accountDestination = fields.String(required=True, nullable=False,
                                       validate=[validate.NoneOf([''], error='Field may not be null.')])
    value = fields.Decimal(required=True, places=2,
                           validate=[validate.Range(min=0, min_inclusive=False, error="Value must be greater then 0.")])
    _id = fields.UUID(missing=uuid.uuid4())
    status = fields.String(missing='in_queue',
                           validate=[validate.OneOf(['in_queue', 'processing', 'confirmed', 'error'])])
    message = fields.String()


class TransferSchemaDump(Schema):
    accountOrigin = fields.String(required=True, nullable=False,
                                  validate=[validate.NoneOf([''], error='Field may not be null.')])
    accountDestination = fields.String(required=True, nullable=False,
                                       validate=[validate.NoneOf([''], error='Field may not be null.')])
    value = fields.Float(required=True,
                         validate=[validate.Range(min=0, min_inclusive=False, error="Value must be greater then 0.")])
    _id = fields.UUID(missing=uuid.uuid4())
    status = fields.String(missing='in_queue',
                           validate=[validate.OneOf(['in_queue', 'processing', 'confirmed', 'error'])])
    message = fields.String()


class IdSchema(Schema):
    transactionId = fields.UUID(required=True, attribute='_id')


class StatusSchema(Schema):
    status = fields.String(required=True)
    message = fields.String()
