import datetime

import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql:///'
database_name = 'picture_metadata_database'


def get_secret_key():
    return os.getenv('SECRET_KEY', 'my_precious_dev')

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = get_secret_key()
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///picture_metadata_database'
