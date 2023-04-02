import pathlib

BOARD_ROW = 6
BOARD_COL = 7
CURRENT_FOLDER = pathlib.Path(__file__).parent
MATCH_DATA_PATH = CURRENT_FOLDER / "matchdata.txt"
MAXIMUM_MOVE = BOARD_COL * BOARD_ROW

# constants for the google cloud
BUCKET_NAME = "result-bucket"
PROJECT_ID = "canvas-sentinel-382020"
REGION = "europe-west1"
INSTANCE_NAME = "instance-1"
DB_NAME = "win_result"
DB_PASS = "test"
INSTANCE_CONNECTION_NAME = f"{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
DB_USER = "annylin3964@gmail.com"
ROLE = "roles/cloudsql.client"

DB_TABLE_NAME = "testtt"
