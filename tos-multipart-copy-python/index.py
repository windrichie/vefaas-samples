import os
import json
import tempfile
import time
from datetime import datetime
import tos

# === CONFIGURABLE VARIABLES ===
ak = "<IAM User Access Key>"  # Replace with your IAM user access key
sk = "<IAM User Secret Key>"  # Replace with your IAM user secret key
endpoint = "tos-ap-southeast-1.ibytepluses.com"  # Replace with your region's TOS endpoint
region = "ap-southeast-1"  # Replace with your region

DEST_BUCKET = "win-test-private-bucket"  # Destination bucket
BASE_PATH = "angt-share"                 # Base path under destination bucket

def handler(event, context):
    print("Received event:")
    print(json.dumps(event, indent=4))

    try:
        # Parse event for source bucket and object key
        src_object_key = event["data"]["events"][0]["tos"]['object']['key']
        src_bucket_name = event["data"]["events"][0]["tos"]['bucket']['name']
        base_file_name = os.path.basename(src_object_key)

        # Generate timestamped destination path
        now = datetime.now()
        date_path = now.strftime("%Y/%m/%d")
        timestamp = str(int(time.time()))
        dest_obj_key = f"{BASE_PATH}/{date_path}/{timestamp}/{base_file_name}"

        print(f"Source: bucket={src_bucket_name}, key={src_object_key}")
        print(f"Destination: bucket={DEST_BUCKET}, key={dest_obj_key}")

        client = tos.TosClientV2(ak, sk, endpoint, region)
        # # Confirm source object exists (optional)
        # client.head_object(src_bucket_name, src_object_key)

        # Multi-part copy with checkpointing
        with tempfile.TemporaryDirectory() as temp_dir:
            checkpoint_file = os.path.join(temp_dir, "copy_checkpoint.json")
            client.resumable_copy_object(
                DEST_BUCKET, dest_obj_key,            # Destination
                src_bucket_name, src_object_key,      # Source
                enable_checkpoint=True,
                part_size=20 * 1024 * 1024,           # 20 MB parts
                checkpoint_file=checkpoint_file
            )

        print(f"Copied file to bucket '{DEST_BUCKET}' key '{dest_obj_key}'")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File copied successfully'})
        }

    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error: {e}'})
        }
