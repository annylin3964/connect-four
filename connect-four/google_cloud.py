from google.cloud import storage

STORAGE_CLIENT = storage.Client()

BUCKET_NAME = "result-bucket"

bucket = STORAGE_CLIENT.create_bucket(BUCKET_NAME)

print(f"Bucket {bucket.name} created.")

