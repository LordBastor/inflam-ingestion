import os
import psycopg2

from psycopg2.extensions import AsIs


class DatabaseCursor(object):
    """
    Provides a DB connection management object
    """

    def __init__(self):
        pass

    def __enter__(self):
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        try:
            # Setup connection
            self.connection = psycopg2.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
                dbname=db_name,
            )

            # Create a cursor instance
            self.cursor = self.connection.cursor()

            # Get or create schema
            candidate_id = AsIs(os.getenv("CANDIDATE_ID"))

            # Creates the candidates schema
            self.cursor.execute("CREATE SCHEMA IF NOT EXISTS %s;", (candidate_id,))

            # Set search path to cursor to make sure
            # we use the correct schema every time
            self.cursor.execute("SET search_path TO %s;", (candidate_id,))

            # Commit the create cursor and search path changes
            self.connection.commit()

            return self.cursor

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
