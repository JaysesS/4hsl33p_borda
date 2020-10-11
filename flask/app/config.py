import os

if os.environ.get('APP_DB_HOST') is None:
    os.environ['APP_DB_HOST'] = "127.0.0.1"
    os.environ['APP_DB_PASSWORD'] = "1337"
    
os.environ['APP_DB_USER'] = "jayse"
os.environ['APP_DB_NAME'] = "borda_db"
os.environ['APP_DB_PORT'] = "3306"

user = os.environ.get('APP_DB_USER')
passwd = os.environ.get('APP_DB_PASSWORD')
host = os.environ.get('APP_DB_HOST')
database = os.environ.get('APP_DB_NAME')
port = os.environ.get('APP_DB_PORT')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}'