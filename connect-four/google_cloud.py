import subprocess


BUCKET_NAME = "result-bucket"
PROJECT_ID = "canvas-sentinel-382020"
REGION = "europe-west1"
INSTANCE_NAME = "instance-1"
DB_NAME = "win_result"
DB_PASS = "test"


# initialize parameters
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"

# grant Cloud SQL Client role to authenticated user
DB_USER = "annylin3964@gmail.com"
ROLE = "roles/cloudsql.client"

subprocess.run(
    [
        "gcloud",
        "projects",
        "add-iam-policy-binding",
        f"{PROJECT_ID}",
        f"--member=user:{DB_USER}",
        f"--role={ROLE}",
    ]
)

# enable cridentials
subprocess.run(["gcloud", "services", "enable", "sqladmin.googleapis.com"])

# create database
subprocess.run(
    [
        "gcloud",
        "sql",
        "databases",
        "create",
        f"{DB_NAME}",
        f"--instance={INSTANCE_NAME}",
    ]
)

# create database user
subprocess.run(
    [
        "gcloud",
        "sql",
        "users",
        "create",
        DB_USER,
        f"--instance={INSTANCE_NAME}",
        f"--password={DB_PASS}",
    ]
)


# configuring credentials
subprocess.run(["gcloud", "auth", "application-default", "login"])


from google.cloud.sql.connector import Connector
import sqlalchemy

# initialize Connector object
connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME, "pg8000", user=DB_USER, password=DB_PASS, db=DB_NAME
    )
    return conn


# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn, future=True,)


# connect to connection pool
with pool.connect() as db_conn:
    # create ratings table in our sandwiches database
    db_conn.execute(
        sqlalchemy.text(
            "CREATE TABLE IF NOT EXISTS ratings "
            "( id SERIAL NOT NULL, name VARCHAR(255) NOT NULL, "
            "origin VARCHAR(255) NOT NULL, rating FLOAT NOT NULL, "
            "PRIMARY KEY (id));"
        )
    )

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    db_conn.commit()

    # insert data into our ratings table
    insert_stmt = sqlalchemy.text(
        "INSERT INTO ratings (name, origin, rating) VALUES (:name, :origin, :rating)",
    )

    # insert entries into table
    db_conn.execute(
        insert_stmt, parameters={"name": "HOTDOG", "origin": "Germany", "rating": 7.5}
    )
    db_conn.execute(
        insert_stmt, parameters={"name": "BÀNH MÌ", "origin": "Vietnam", "rating": 9.1}
    )
    db_conn.execute(
        insert_stmt,
        parameters={"name": "CROQUE MADAME", "origin": "France", "rating": 8.3},
    )

    # commit transactions
    db_conn.commit()

    # query and fetch ratings table
    results = db_conn.execute(sqlalchemy.text("SELECT * FROM ratings")).fetchall()

    # show results
    for row in results:
        print(row)


# from google.cloud.sql.connector import Connector
# import sqlalchemy
# import pymysql

# # initialize Connector object
# connector = Connector()

# # function to return the database connection
# def getconn() -> pymysql.connections.Connection:
#     conn: pymysql.connections.Connection = connector.connect(
#         INSTANCE_CONNECTION_NAME,
#         "pymysql",
#         user="my-user",
#         password="",
#         db="test"
#     )
#     return conn

# # create connection pool
# pool = sqlalchemy.create_engine(
#     "mysql+pymysql://",
#     creator=getconn,
# )

# # insert statement
# insert_stmt = sqlalchemy.text(
#     "INSERT INTO my_table (id, title) VALUES (:id, :title)",
# )

# with pool.connect() as db_conn:
#     # insert into database
#     db_conn.execute(insert_stmt, parameters={"id": "book1", "title": "Book One"})

#     # query database
#     result = db_conn.execute(sqlalchemy.text("SELECT * from my_table")).fetchall()

#     # commit transaction (SQLAlchemy v2.X.X is commit as you go)
#     db_conn.commit()

#     # Do something with the results
#     for row in result:
#         print(row)

# connector.close()
