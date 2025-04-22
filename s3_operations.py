"""Provides functionaties to add, fetch and delete S3 objects based on specific tags or metadata."""

import os
from os.path import dirname, join

import boto3

script_dir = dirname(__file__)


class S3Operations:
    """class for adding, fetching and deleting objects with tags and metadata in s3 bucket."""

    def __init__(self, bucket_name, region_name):
        """Initialize an instance of S3Operations class."""
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3_client = boto3.client("s3", region_name=self.region_name)

    def add_s3_objects(self, no_of_objects):
        """Add objects with tags and metadata to s3 bucket."""
        for i in range(no_of_objects):
            tags, meta_data = self.generate_tags_metadata(i)
            tags_str = "&".join(f"{key}={value}" for key, value in tags.items())

            filename = "data" + str(i) + ".txt"
            filepath = join(script_dir, filename)
            with open(filepath, "w") as file:
                file.write("text document " + str(i))
            file.close()

            self.s3_client.upload_file(
                filepath,
                self.bucket_name,
                filename,
                ExtraArgs={"Metadata": meta_data, "Tagging": tags_str},
            )

            # print(f"{filename} uploaded!")
            os.remove(filepath)
        print("All files uploaded successfully")

    def generate_tags_metadata(self, i):
        """Generate tags and metadata based on condition.

        Args:
            i (int): value to check

        Returns:
            dict: tags
            dict: meta_data
        """
        tags = dict()
        meta_data = dict()
        if i < 1500:
            tags["tagA"] = "10"
            meta_data = {"meta_key": "1500"}

        elif i >= 1500 and i < 2000:
            tags["tagB"] = "20"
            meta_data = {"meta_key": "2000"}
        else:
            tags["tagC"] = "30"
            meta_data = {"meta_key": "2500"}

        return tags, meta_data

    def get_objects(self):
        """Return the list of keys of objects present in the s3 bucket.

        Returns:
            list: objects
        """
        objects = []
        paginator = self.s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=self.bucket_name)

        for page in page_iterator:
            for object in page["Contents"]:
                obj_key = object["Key"]
                objects.append(obj_key)

        return objects

    def save_file(self, output_filename, output):
        """Save all items of list to a text file.

        Args:
            output_filename (str): filename of output text file
            output (list): list of items to save
        """
        output_dir = "output/"
        os.makedirs(output_dir, exist_ok=True)
        with open(join(output_dir, output_filename), "w") as file:
            for item in output:
                file.write(item)
                file.write("\n")

    def fetch_s3_objects_by_tags(self, tag_key, tag_val):
        """Filter s3 objects by tags(tag_key & tag_val) and save filtered object keys into a txt file.

        Args:
            tag_key (str): key of a tag used to filter s3 objects
            tag_val (str): value of a tag used to filter s3 objects
        """
        output = []
        objects = self.get_objects()

        print("filtering objects by tags...")
        for obj_key in objects:
            tags = self.s3_client.get_object_tagging(
                Bucket=self.bucket_name, Key=obj_key
            )["TagSet"]

            for tag in tags:
                if tag["Key"] == tag_key and str(tag["Value"]) == str(tag_val):
                    output.append(obj_key)
        output_filename = "output-tag-" + str(tag_key) + "-" + str(tag_val) + ".txt"
        self.save_file(output_filename, output)
        print(
            f"{len(output)} files fetched successfully with tag {tag_key} = {tag_val}"
        )

    def fetch_s3_objects_by_metadata(self, key, val):
        """Filter s3 objects by metadata(key & val) and save filtered object keys into a txt file.

        Args:
            key (str): key of a metdata used to filter s3 objects
            val (str): value of a metadata used to filter s3 objects
        """
        output = []
        objects = self.get_objects()

        print("filtering objects by metadata...")
        for obj_key in objects:
            metadata = self.s3_client.head_object(Bucket=self.bucket_name, Key=obj_key)[
                "Metadata"
            ]

            for k, v in metadata.items():
                if k == key and str(v) == str(val):
                    output.append(obj_key)

        output_filename = "output-metadata-" + str(key) + "-" + str(val) + ".txt"
        self.save_file(output_filename, output)
        print(f"{len(output)} files fetched successfully with metadata {key} = {val}")

    def delete_s3_objects_by_tags(self, tag_key, tag_val):
        """Filter s3 objects by tags(key & val) and delete filtered objects.

        Args:
            tag_key (str): key of a tag used to filter s3 objects
            tag_val (str): value of a tag used to filter s3 objects
        """
        output = []
        objects = self.get_objects()

        print("filtering objects by tags...")
        for obj_key in objects:
            tags = self.s3_client.get_object_tagging(
                Bucket=self.bucket_name, Key=obj_key
            )["TagSet"]

            for tag in tags:
                if tag["Key"] == tag_key and str(tag["Value"]) == str(tag_val):
                    output.append(obj_key)

        for item in output:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=item)
        print(f"{len(output)} files deleted succesfully with tag {tag_key} = {tag_val}")

    def delete_s3_objects_by_metadata(self, key, val):
        """Filter s3 objects by metadata(key & val) and delete filtered objects.

        Args:
            key (str): key of a metdata used to filter s3 objects
            val (str): value of a metdata used to filter s3 objects
        """
        output = []
        objects = self.get_objects()

        print("filtering objects by metadata...")
        for obj_key in objects:
            metadata = self.s3_client.head_object(Bucket=self.bucket_name, Key=obj_key)[
                "Metadata"
            ]

            for k, v in metadata.items():
                if k == key and str(v) == str(val):
                    output.append(obj_key)

        for item in output:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=item)
        print(f"{len(output)} files deleted succesfully with metadata {key} = {val}")

    def total_objects(self):
        """Print total number of objects present in the s3 bucket."""
        s3_resource = boto3.resource("s3", region_name="ap-south-1")
        count = 0
        for obj in s3_resource.Bucket(self.bucket_name).objects.all():
            count += 1
        print("Total Objects in bucket: ", count)


if __name__ == "__main__":

    NO_OF_OBJECTS = 2500
    BUCKET_NAME = "data-bucket-s797866"
    REGION_NAME = "ap-south-1"

    obj = S3Operations(bucket_name=BUCKET_NAME, region_name=REGION_NAME)

    # obj.add_s3_objects(NO_OF_OBJECTS)

    obj.fetch_s3_objects_by_tags("tagB", 20)
    obj.fetch_s3_objects_by_tags("tagA", 10)
    obj.fetch_s3_objects_by_tags("tagC", 30)

    obj.fetch_s3_objects_by_metadata("meta_key", 2000)
    obj.fetch_s3_objects_by_metadata("meta_key", 1500)
    obj.fetch_s3_objects_by_metadata("meta_key", 2500)

    # obj.delete_s3_objects_by_tags("tagC", 30)
    # obj.delete_s3_objects_by_tags("tagA", 10)

    # obj.delete_s3_objects_by_metadata("meta_key", 1500)

    obj.total_objects()
