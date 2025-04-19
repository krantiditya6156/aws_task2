import json
import os
from os.path import dirname, join

import boto3


NO_OF_OBJECTS = 2500
FILE_NAME = "data"
BUCKET_NAME = "data-bucket-s797866"

script_dir = dirname(__file__)



s3_client = boto3.client('s3', region_name="ap-south-1")

class S3Operations:

    def __init__(self):
        pass

    
    def add_s3_objects(self):  
    
        for i in range(NO_OF_OBJECTS):
            tags, meta_data = self.generate_tags_metadata(i)
            tags_str = "&".join(f"{key}={value}" for key, value in tags.items())

            filename = FILE_NAME + str(i) + ".txt"
            filepath = join(script_dir, filename)
            with open(filename, "w") as file:
                file.write("text document " + str(i))
            file.close()
            
            s3_client.upload_file(filepath, 
                                    BUCKET_NAME, 
                                    filename,  
                                    ExtraArgs={'Metadata': meta_data, 
                                                'Tagging': tags_str})

            # print(f"{filename} uploaded!")
            os.remove(filepath)
        print("All files uploaded successfully")


    def generate_tags_metadata(self, i):
        tags = dict()
        meta_data = dict()
        if i<1500:
            tags['tagA'] = "10"
            meta_data = {"meta_key":"1500"}

        elif i>=1500 and i<2000:
            tags['tagB'] = "20"
            meta_data = {"meta_key":"2000"}
        else:
            tags['tagC'] = "30"
            meta_data = {"meta_key":"2500"}

        return tags, meta_data

    def get_objects(self):
        objects = []
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=BUCKET_NAME)

        for page in page_iterator:
            for object in page['Contents']:
                obj_key = object['Key']
                objects.append(obj_key)
              
        return objects
        
    def save_file(self, output_filename, output):
        with open(output_filename, "w") as file:
            for item in output:
                file.write(item)
                file.write("\n")

    def fetch_s3_objects_by_tags(self, tag_key, tag_val):
        output = []
        objects = self.get_objects()
        
        print("filtering objects by tags...")
        for obj_key in objects:
            tags = s3_client.get_object_tagging(Bucket=BUCKET_NAME, Key=obj_key)['TagSet']

            for tag in tags:
                if tag['Key']==tag_key and str(tag['Value'])==str(tag_val):
                    output.append(obj_key)
        output_filename = "output-tag-" + str(tag_key) + "-" + str(tag_val) + ".txt"
        self.save_file(output_filename, output)
        print(f"{len(output)} files fetched successfully with tag {tag_key} = {tag_val}")
        
                
    def fetch_s3_objects_by_metadata(self, key, val):
        output = []
        objects = self.get_objects()

        print("filtering objects by metadata...")
        for obj_key in objects:
            metadata = s3_client.head_object(Bucket=BUCKET_NAME, Key=obj_key)['Metadata']

            for k, v in metadata.items():
                if k==key and str(v)==str(val):
                    output.append(obj_key)            
            
        output_filename = "output-metadata-" + str(key) + "-" + str(val) + ".txt"
        self.save_file(output_filename, output)
        print(f"{len(output)} files fetched successfully with metadata {key} = {val}")
        

    def delete_s3_objects_by_tags(self, tag_key, tag_val):
        output = []
        objects = self.get_objects()

        print("filtering objects by tags...")
        for obj_key in objects:
            tags = s3_client.get_object_tagging(Bucket=BUCKET_NAME, Key=obj_key)['TagSet']

            for tag in tags:
                if tag['Key']==tag_key and str(tag['Value'])==str(tag_val):
                    output.append(obj_key)

        for item in output:
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=item)
        print(f"{len(output)} files deleted succesfully with tag {tag_key} = {tag_val}")


    def delete_s3_objects_by_metadata(self, key, val):
        output = []
        objects = self.get_objects()

        print("filtering objects by metadata...")
        for obj_key in objects:
            metadata = s3_client.head_object(Bucket=BUCKET_NAME, Key=obj_key)['Metadata']

            for k, v in metadata.items():
                if k==key and str(v)==str(val):
                    output.append(obj_key)

        for item in output:
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=item)
        print(f"{len(output)} files deleted succesfully with metadata {key} = {val}")        


    def total_objects(self):
        s3_resource = boto3.resource('s3', region_name="ap-south-1")
        count = 0
        for obj in s3_resource.Bucket(BUCKET_NAME).objects.all():
            count+=1
        print("Total Objects in bucket: ", count)



if __name__ == "__main__":

    obj = S3Operations()


    obj.add_s3_objects()


    # obj.fetch_s3_objects_by_tags("tagB", 20)
    # obj.fetch_s3_objects_by_tags("tagA", 10)
    # obj.fetch_s3_objects_by_tags("tagC", 30)

    # obj.fetch_s3_objects()

    # obj.fetch_s3_objects_by_metadata("meta_key", 2000)



    # obj.delete_s3_objects_by_tags("tagC", 30)
    # obj.delete_s3_objects_by_tags("tagA", 10)

    # obj.delete_s3_objects_by_metadata("meta_key", 1500)

    obj.total_objects()