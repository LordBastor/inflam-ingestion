# Running the ingestion locally

- Setup a python 3.6+ virtual env by `python3 -m venv env` or your virtual env wrapper of choice
- Activate the virtualenv `source env/bin/activate`
- Setup the requirements `pip install -r requirements.txt`

The commands you can run afterwards are as follows:
- `python main.py download` - downloads the CSV to the local filesystem
- `python main.py upload_s3` - uploads the CSV to the s3 bucket
- `python main.py upload_db` - uploads the CSV from the buckets to the DB


# Building the docker image
- Build the image using `docker build -t infinite-lambda-ingestion:latest .` (or whatever naming you may be fond of)
- Run the image by using `docker run infinite-lambda-ingestion:latest`
