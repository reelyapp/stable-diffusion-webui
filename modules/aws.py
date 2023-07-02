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

# TODO: Get username and 
def put_image(ulid):
    dynamodb = boto3.client('dynamodb', region_name="us-west-2" )
    # Replace 'YOUR_TABLE_NAME' with the actual name of your DynamoDB table
    # TODO
    table_name = "advertisement-table-staging"

    # Data to be inserted or updated in the DynamoDB table
    item = {
        "pk": {"S": f"IMAGE#{ulid}"},  # Assuming primary_key is of string type
        "sk": {"S": f"IMAGE#{ulid}"},
        "gs1pk": {"S": f"IMAGE#{ulid}"},
        "gs1sk": {"S": f"IMAGE#{ulid}"},
        "url": {"S": f"https://ad-creator-generated-images.s3.us-west-2.amazonaws.com/{ulid}"},
    }

    # Put the item into the DynamoDB table
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )


def upload_base64_image(image):
    ulid = ULID()
    s3_client = boto3.client('s3')
    binary_content = base64.b64decode(image)
    s3_client.put_object(Bucket=BUCKET, Key=str(ulid), Body=binary_content)
    return ulid

# if __name__ == "__main__":
#     upload_image()
