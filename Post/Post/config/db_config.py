import os

def Build_Database_uri(username, password, host):
    try:
        database_uri = "mysql+pymysql://" + username + ":" + password + "@" + host
    except:
        database_uri = ""
    return database_uri

class LocalDBConfig:
    LOCAL_DATABASE_USERNAME = "root"
    LOCAL_DATABASE_PASSWORD = os.getenv("LOCAL_DATABASE_PASSWORD")
    LOCAL_DATABASE_HOST = os.getenv("LOCAL_DATABASE_HOST")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = Build_Database_uri(
        LOCAL_DATABASE_USERNAME, LOCAL_DATABASE_PASSWORD, LOCAL_DATABASE_HOST
    )

