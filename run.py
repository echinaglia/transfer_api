from api import factory

app = factory.flask
celery = factory.celery
mongo = factory.mongo

if __name__ == '__main__':
    app.run()
