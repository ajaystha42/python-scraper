from dotenv import dotenv_values

config = dotenv_values(".env")

DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']
DB_USERNAME = config['DB_USERNAME']
DB_PASSWORD = config['DB_PASSWORD']
DB_NAME = config['DB_NAME']
POSTED_BY = config['POSTED_BY']
TAG = config['TAG']
