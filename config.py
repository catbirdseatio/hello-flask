import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_ENV = "development"
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'test.db')}")

