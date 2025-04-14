import boto3, os
from os.path import dirname, join

NO_OF_OBJECTS = 20
FILE_NAME = "data"
BUCKET_NAME = "data-bucket-s797866"

script_dir = dirname(__file__)

def add_s3_objects():

    s3_client = boto3.client('s3', region_name="ap-south-1")
    
    for i in range(NO_OF_OBJECTS):
        filename = FILE_NAME + str(i) + ".txt"
        filepath = join(script_dir, filename)
        with open(filename, "w") as file:
            file.write("text document " + str(i))
        file.close()
        s3_client.upload_file(filepath, 
                              BUCKET_NAME, 
                              filename,  
                              ExtraArgs={'Metadata': {'meta_key': '678'}                                         
                                         })
        print(f"{filename} uploaded!")
        os.remove(filepath)


if __name__ == "__main__":
    add_s3_objects()