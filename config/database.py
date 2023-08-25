import json

FETCH_POSTS = 'select ext_properties from post where post."tagId" = 2'
INSERT_JOB = '''
INSERT INTO 
"post"("post", "ext_properties", "postedById", "tagId") 
VALUES (%s, %s, 694, 2) 
'''
# Replace job_id with post_id after job_id column has been added to the post table
# FETCH_POSTS = 'select job_id from post where post."tagId" = 2'
# RETURNING id
# RETURNING "post_id", "postAs", "whoLikes", "likesQty", "taggedUsers", "isDeleted", "createdAt", "postedById", "updatedAt", "reportReason", "isFreezed", "actionTakenBy"


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
    cursor.executemany(INSERT_JOB, data)
    print('All data inserted successfully.')
