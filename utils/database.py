
import constants.queries as queries


# Replace job_id with post_id after job_id column has been added to the post table
# FETCH_POSTS = 'select job_id from post where post."tagId" = 2'
# RETURNING id
# RETURNING "post_id", "postAs", "whoLikes", "likesQty", "taggedUsers", "isDeleted", "createdAt", "postedById", "updatedAt", "reportReason", "isFreezed", "actionTakenBy"


def fetch_posts(cursor):
    try:
        cursor.execute(queries.FETCH_POSTS)
        results = cursor.fetchall()

        valid_data = []

        for item in results:
            if item[0] is not None:
                valid_data.append(int(item[0]['job_id']))
        posts = set(valid_data)
        return posts
    except Exception as e:
        print('Exception ', e)


def insert_jobs(cursor, data):
    try:
        cursor.executemany(queries.INSERT_JOB, data)
        print('All data inserted successfully.')
    except Exception as e:
        print('Exception ', e)
