import boto3
import csv
import os
import requests
import sys

from db_connection import DatabaseCursor
from dotenv import load_dotenv


# Sets up environment variables from .env file
load_dotenv()

AWS_BUCKET = os.getenv("AWS_BUCKET")
AWS_REGION = os.getenv("AWS_REGION")
AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")

CSV_FILE_NAME = "Mall_Customers.csv"
CANDIDATE_ID = os.getenv("CANDIDATE_ID")
FILE_PATH = "{}/{}".format(CANDIDATE_ID, CSV_FILE_NAME)


def get_boto3_client(resource_name):
    """
    Returns a boto3 client for the specified resource name
    Safe for repeat-calls since this is just a proxy to a singleton session
    """

    return boto3.resource(
        resource_name,
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET,
        region_name=AWS_REGION,
    )


def download_csv():
    """
    Ingests the csv data and saves it to the filesystem
    """

    csv_url = (
        "https://raw.githubusercontent.com/SteffiPeTaffy/machineLearningAZ"
        "/master/Machine%20Learning%20A-Z%20Template%20Folder/Part%204%20-"
        "%20Clustering/Section%2025%20-%20Hierarchical%20Clustering/Mall_C"
        "ustomers.csv"
    )

    # Make a request call to grab the csv data
    response = requests.get(csv_url)

    # Write respose content to a file
    with open(CSV_FILE_NAME, "w") as file:
        writer = csv.writer(file)
        first_line = True
        for line in response.iter_lines():
            # Skip the first
            if first_line:
                first_line = False
                continue
                line = "customer_id,gender,age,annual_income,spending_score"
                writer.writerow(line.split(","))

            writer.writerow(line.decode("utf-8").split(","))


def upload_csv_to_s3():
    """
    Uploads the csv to a predifined s3 bucket
    """

    # Get the s3 client and bucket
    s3 = get_boto3_client("s3")
    s3.Bucket(AWS_BUCKET)

    # PUT the object into the bucket
    s3.Object(AWS_BUCKET, FILE_PATH,).put(Body=open("{}".format(CSV_FILE_NAME), "rb"))


def upload_to_db():
    """
    Uploads the ingested CSV to a database
    """

    with DatabaseCursor() as cursor:
        # Setup the database table or make sure it's already there
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS mall_customers(
                    customer_id INT PRIMARY KEY NOT NULL,
                    gender char(6),
                    age smallint,
                    annual_income smallint,
                    spending_score smallint
                );
            """
        )

        cursor.connection.commit()

        # Setup the ingestion from s3 to out rds postgres
        cursor.execute(
            "SELECT aws_s3.table_import_from_s3(%s, '', '(format csv)', %s, %s, %s)",
            ("bg200320.mall_customers", AWS_BUCKET, FILE_PATH, AWS_REGION),
        )

        cursor.connection.commit()


if __name__ == "__main__":
    command = None

    if len(sys.argv) >= 2:
        command = sys.argv[1]

    if command == "download":
        download_csv()

    if command == "upload_s3":
        upload_csv_to_s3()

    if command == "upload_db":
        upload_to_db()
