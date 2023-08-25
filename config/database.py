FETCH_POSTS = 'select post_id from post where post."tagId" = 2'
INSERT_JOB = 'INSERT INTO post (post, posted_by) VALUES (%s, %s)'
# Replace job_id with post_id after job_id column has been added to the post table
# FETCH_POSTS = 'select job_id from post where post."tagId" = 2'
# RETURNING id


def fetch_posts(cursor):
    cursor.execute(FETCH_POSTS)
    results = cursor.fetchall()
    posts = set(item[0] for item in results)
    return posts


def insert_jobs(cursor, data):
    cursor.executemany(INSERT_JOB, data)
    print('All data inserted successfully.')
