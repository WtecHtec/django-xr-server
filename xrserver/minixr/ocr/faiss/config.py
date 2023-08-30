from os import abort
# import psycopg2
import pymsql

HOSTNAME = '9.134.163.223'
USERNAME = 'root'
PASSWORD = 'Apc@portal168'
DATABASE_NAME = 'minixr'
PORT = 3306



def get_postgres_connection():
    try:
        connection = pymsql.connect(
            user=USERNAME,
            password=PASSWORD,
            host=HOSTNAME,
            port=PORT,
            database=DATABASE_NAME,
            
            )
        return connection
    except (Exception, pymsql.Error) as error:
        message = f"get_postgres_connection {error}"
        return abort(400, message)
