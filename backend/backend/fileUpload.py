# postgreSQL database adapter
import psycopg2

import os

# connecting to postgreSQL
# database: django.db.backends.postgresql
conn = psycopg2.connect(database='ColPalDB',
                        user=os.environ.get('DB_USER'),
                        password=os.environ.get('DB_PASS'),
                        host=os.environ.get('DB_HOST'),
                        port=os.environ.get('DB_PORT'))

conn.autocommit = True
cursor = conn.cursor()

# creating table
sql = ''' table '''

cursor.execute(sql)

# copy to add path to csv file
sqlcpy = ''' COPY 
            FROM
            DELIMITER
            CSV HEADER '''

cursor.execute(sqlcpy)

