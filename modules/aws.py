import logging
import boto3
import base64
from ulid import ULID
from botocore.exceptions import ClientError
import os
from PIL import Image

BUCKET = 'ad-creator-generated-images';

# Check if I still need this. maybe even as an environment variable?
os.environ['AWS_PROFILE'] = "reelyapp"

def dynamodb_put(ulid: str, username: str, advertisment_id: str):
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
    dynamodb.put_item(
        TableName=table_name,
        Item=item
    )

def s3_upload(base64Img: bytes):
    ulid = ULID()
    s3_client = boto3.client('s3')
    binary_content = base64.b64decode(base64Img)
    s3_client.put_object(Bucket=BUCKET, Key=str(ulid), Body=binary_content)
    return str(ulid)

