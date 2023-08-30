from os import abort
import pymysql

# HOSTNAME = '9.134.163.223'
# USERNAME = 'root'
# PASSWORD = 'Apc@portal168'
# DATABASE_NAME = 'minixr'
# PORT = 3306

HOSTNAME = '1.116.139.149'
USERNAME = 'root'
PASSWORD = 'oneX8748'
DATABASE_NAME = 'web_note'
PORT = 3306



def get_postgres_connection():
    try:
        connection = pymysql.connect(
            user=USERNAME,
            password=PASSWORD,
            host=HOSTNAME,
            port=PORT,
            database=DATABASE_NAME)
        return connection
    except (Exception, pymysql.Error) as error:
        message = f"get_postgres_connection {error}"
        return abort(400, message)
