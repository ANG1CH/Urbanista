import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = 'static/upload'
    SERVER_PATH = os.path.join(ROOT, UPLOAD_PATH)

    USER = os.environ.get('POSTGRES_USER', 'angich')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'lohotron')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5532)
    DB = os.environ.get('POSTGRES_DB', 'urbanista_db')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    SECRET_KEY = 'apwtJOI86p3VmLHoi7arNRTRbaLn6Buu3ASpliap'
    SQLALCHEMY_TRACK_MODIFICATIONS = True