import logging
import boto3
from botocore.exceptions import ClientError
import os

BUCKET = 'ad-creator-generated-images';

os.environ['AWS_PROFILE'] = "reelyapp"

def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, BUCKET, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# def put_image(image, object_name=None):
#     """Upload a file to an S3 bucket

#     :param image: Image to upload
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.put_object(Bucket=BUCKET, Key=object_name, Body=image)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True

if __name__ == "__main__":
    upload_file('test.jpeg')
