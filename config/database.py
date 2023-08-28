import psycopg2
from psycopg2 import Error

# FOR LOCAL DB
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USERNAME = 'postgres'
DB_PASSWORD = 'Aj@y'
DB_NAME = 'husslup'


# FETCH_POSTS = 'select ext_properties from post where post."tagId" = 2'
FETCH_POSTS = '''
select "post"."ext_properties" from "post" where "post"."tagId" = 2 
and "post"."ext_properties" is not null
'''
INSERT_JOB = '''
INSERT INTO 
"post"("post", "ext_properties", "postedById", "tagId") 
VALUES (%s, %s, 694, 2) 
'''
# Replace job_id with post_id after job_id column has been added to the post table
# FETCH_POSTS = 'select job_id from post where post."tagId" = 2'
# RETURNING id
# RETURNING "post_id", "postAs", "whoLikes", "likesQty", "taggedUsers", "isDeleted", "createdAt", "postedById", "updatedAt", "reportReason", "isFreezed", "actionTakenBy"


def create_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            port=str(DB_PORT)
        )
        print("Connected to the database successfully")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def fetch_posts(cursor):
    cursor.execute(FETCH_POSTS)
    results = cursor.fetchall()

    valid_data = []

    for item in results:
        if item[0] is not None:
            valid_data.append(int(item[0]['job_id']))
    posts = set(valid_data)
    return posts


def insert_jobs(cursor, data):
    try:
        cursor.executemany(INSERT_JOB, data)
        print('All data inserted successfully.')
    except Exception as e:
        print('Exception ', e)
