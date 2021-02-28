import os

from celery import Celery
from flask import Flask
from pymongo import MongoClient

from api.config import config


class Factory(object):
    """Build the instances needed for the API."""

    def __init__(self, environment='default'):
        """Initialize Factory with the proper environment."""
        # Get the running environment
        self._environment = os.getenv("APP_ENVIRONMENT")
        if not self._environment:
            self._environment = environment

    @property
    def environment(self):
        """Getter for environment attribute."""
        return self._environment

    @environment.setter
    def environment(self, environment):
        # Update environment protected variable
        self._environment = environment

        # Update Flask configuration
        self.flask.config.from_object(config[self._environment])

        # Update Celery Configuration
        self.celery.conf.update(self.flask.config)

    def set_flask(self, **kwargs):
        """Flask instantiation."""
        # Flask instance creation
        self.flask = Flask(__name__, **kwargs)

        # Flask configuration
        self.flask.config.from_object(config[self._environment])

        # Swagger documentation
        self.flask.config.SWAGGER_UI_DOC_EXPANSION = 'list'
        self.flask.config.SWAGGER_UI_JSONEDITOR = True

        return self.flask

    def set_celery(self, **kwargs):
        """Celery instantiation."""
        # Celery instance creation
        self.celery = Celery(__name__, **kwargs)

        # Celery Configuration
        self.celery.conf.update(self.flask.config)

        return self.celery

    def register(self, blueprint):
        """Register a specified blueprint."""
        self.flask.register_blueprint(blueprint)

    def set_mongo(self, **kwargs):
        self.mongo = MongoClient('mongodb', 27017, connect=False)
        self.db = self.mongo.transfer_db
