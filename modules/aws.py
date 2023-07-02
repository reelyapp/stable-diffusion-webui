import logging
import boto3
import base64
from ulid import ULID
from botocore.exceptions import ClientError
import os
from PIL import Image

BUCKET = 'ad-creator-generated-images';

os.environ['AWS_PROFILE'] = "reelyapp"

def upload_image(file_name, image, object_name=None):
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
        # response = s3_client.upload_file(file_name, BUCKET, object_name)
        with open(file_name, "rb") as f:
               image_data = f.read()

        response = s3_client.put_object(Bucket=BUCKET, Key=file_name, Body=image_data)
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
    # s3_client = boto3.client('s3')
#     try:
#         response = s3_client.put_object(Bucket=BUCKET, Key=object_name, Body=image)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True

# def upload_image():
#     local_image_path = "pil_test.jpg"
#     pil_image = Image.open(local_image_path)
#     upload_file(local_image_path, pil_image)


def upload_base64_image(image):
    ulid = ULID()
    s3_client = boto3.client('s3')
    binary_content = base64.b64decode(image)
    s3_client.put_object(Bucket=BUCKET, Key=ulid, Body=binary_content)
    return ulid

# if __name__ == "__main__":
#     upload_image()
