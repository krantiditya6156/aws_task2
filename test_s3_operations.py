import unittest

import boto3
from moto import mock_aws

from s3_operations import S3Operations


@mock_aws
class TestS3Operations(unittest.TestCase):

    def setUp(self):
        print("In setup class")
        self.s3client = boto3.client("s3", region_name="ap-south-1")
        self.s3client.create_bucket(
            Bucket="mock_bucket",
            CreateBucketConfiguration={"LocationConstraint": "ap-south-1"},
        )
        self.s3obj = S3Operations(bucket_name="mock_bucket", region_name="ap-south-1")

    def tearDown(self):
        return super().tearDown()

    def test_add_s3_objects(self):

        self.s3obj.add_s3_objects(2500)
        objects = self.s3obj.get_objects()
        self.assertEqual(len(objects), 2500)

    def test_fetch_s3_objects_by_tags(self):

        self.s3obj.add_s3_objects(2500)

        self.s3obj.fetch_s3_objects_by_tags("tagA", 10)
        with open("output/output-tag-tagA-10.txt", "r") as file:
            content = file.readlines()
            self.assertEqual(len(content), 1500)

        self.s3obj.fetch_s3_objects_by_tags("tagB", 20)
        with open("output/output-tag-tagB-20.txt", "r") as file:
            content = file.readlines()
            self.assertEqual(len(content), 500)

        self.s3obj.fetch_s3_objects_by_tags("tagC", 30)
        with open("output/output-tag-tagC-30.txt", "r") as file:
            content = file.readlines()
            self.assertEqual(len(content), 500)

    def test_fetch_s3_objects_by_metadata(self):

        self.s3obj.add_s3_objects(2500)

        self.s3obj.fetch_s3_objects_by_metadata("meta_key", 1500)
        with open("output/output-metadata-meta_key-1500.txt", "r") as file:
            content = file.readlines()
            self.assertEqual(len(content), 1500)

        self.s3obj.fetch_s3_objects_by_metadata("meta_key", 2000)
        with open("output/output-metadata-meta_key-2000.txt", "r") as file:
            content = file.readlines()
            self.assertEqual(len(content), 500)

        self.s3obj.fetch_s3_objects_by_metadata("meta_key", 2500)
        with open("output/output-metadata-meta_key-2500.txt", "r") as file:
            content = file.readlines()
            self.assertEqual(len(content), 500)

    def test_delete_s3_objects_by_tags(self):
        self.s3obj.add_s3_objects(2500)

        self.s3obj.delete_s3_objects_by_tags("tagA", 10)
        total_objects_in_bucket = self.s3obj.total_objects()
        self.assertEqual(total_objects_in_bucket, 1000)

        self.s3obj.delete_s3_objects_by_tags("tagB", 20)
        total_objects_in_bucket = self.s3obj.total_objects()
        self.assertEqual(total_objects_in_bucket, 500)

        self.s3obj.delete_s3_objects_by_tags("tagC", 30)
        total_objects_in_bucket = self.s3obj.total_objects()
        self.assertEqual(total_objects_in_bucket, 0)

    def test_delete_s3_objects_by_metadata(self):
        self.s3obj.add_s3_objects(2500)

        self.s3obj.delete_s3_objects_by_metadata("meta_key", 1500)
        total_objects_in_bucket = self.s3obj.total_objects()
        self.assertEqual(total_objects_in_bucket, 1000)

        self.s3obj.delete_s3_objects_by_metadata("meta_key", 2000)
        total_objects_in_bucket = self.s3obj.total_objects()
        self.assertEqual(total_objects_in_bucket, 500)

        self.s3obj.delete_s3_objects_by_metadata("meta_key", 2500)
        total_objects_in_bucket = self.s3obj.total_objects()
        self.assertEqual(total_objects_in_bucket, 0)


if __name__ == "__main__":
    unittest.main()
