import os

if os.environ.get('APP_DB_HOST') is None:
    os.environ['APP_DB_HOST'] = "***"
    os.environ['APP_DB_PASSWORD'] = "***"
    
os.environ['APP_DB_USER'] = "***"
os.environ['APP_DB_NAME'] = "***"
os.environ['APP_DB_PORT'] = "***"

user = os.environ.get('APP_DB_USER')
passwd = os.environ.get('APP_DB_PASSWORD')
host = os.environ.get('APP_DB_HOST')
database = os.environ.get('APP_DB_NAME')
port = os.environ.get('APP_DB_PORT')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}'