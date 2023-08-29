import config.config as config

# Enum
PUBLISH_STATUS = "pending_review"


FETCH_POSTS = '''
SELECT "post"."ext_properties"
FROM "post" WHERE "post"."tagId" = 2 
AND "post"."ext_properties" IS NOT NULL
'''

INSERT_JOB = f'''INSERT INTO 
"post"("post", "ext_properties", "publish_status", "postedById", "tagId") 
VALUES (%s, %s, '{PUBLISH_STATUS}', {config.POSTED_BY}, {config.TAG})'''
