"""Provides two instances of a filestore.

There is not intended to be any vulnerability contained within this code. This file is provided to
make it easier to test locally without needing access to an S3 bucket.

-OOO

"""
import os

import boto3
import botocore


class NotFound(Exception):
    pass


class LocalStore:
    def __init__(self):
        import tempfile
        self.upload_directory = tempfile.mkdtemp()

    def read(self, key):
        filepath = os.path.join(self.upload_directory, key)

        try:
            with open(filepath, "rb") as fp:
                return fp.read()
        except FileNotFoundError:
            raise NotFound

    def save(self, key, data):
        with open(os.path.join(self.upload_directory, key), "wb") as fp:
            fp.write(data)


class S3Store:
    """Credentials grant access only to resource s3://BUCKET/* and only for:

    * GetObject
    * PutObject

    """

    def __init__(self):
        self.bucket = os.environ["BUCKET"]
        self.s3 = boto3.client("s3")

    def read(self, key):
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
        except botocore.exceptions.ClientError as exception:
            if exception.response["ResponseMetadata"]["HTTPStatusCode"] == 403:
                raise NotFound
            # No other exceptions encountered during testing
        return response["Body"].read()

    def save(self, key, data):
        self.s3.put_object(
            Body=data, Bucket=self.bucket, ContentType="text/plain", Key=key
        )
