import os
import json
import tempfile
from PIL import Image
import tos

ak = "<IAM User Access Key>" # Replace with your IAM user access key
sk = "<IAM User Secret Key>" # Replace with your IAM user secret key
endpoint = "tos-ap-southeast-1.ibytepluses.com" # Replace with your region's TOS endpoint
region = "ap-southeast-1" # Replace with your region

destination_prefix = "resized"

def handler(event, context):
    print("Received event:")
    print(json.dumps(event, indent=4))

    object_key = event["data"]["events"][0]["tos"]['object']['key']
    bucket_name = event["data"]["events"][0]["tos"]['bucket']['name']
    base_file_name = os.path.basename(object_key)
    name, ext = os.path.splitext(base_file_name)

    if ext.lower() not in [".jpg", ".jpeg", ".png"]:
        print(f"Unsupported file type: {ext}")
        return

    if object_key.startswith(destination_prefix):
        print("Already processed, skipping.")
        return

    temp_dir = tempfile.TemporaryDirectory()
    input_path = os.path.join(temp_dir.name, base_file_name)
    output_file_name = f"{name}.webp"
    output_path = os.path.join(temp_dir.name, output_file_name)

    try:
        client = tos.TosClientV2(ak, sk, endpoint, region)
        print(f"Downloading {object_key} from bucket {bucket_name}")
        client.get_object_to_file(bucket_name, object_key, input_path)

        print(f"Resizing and converting image to WebP: {input_path}")
        with Image.open(input_path) as img:
            new_size = (int(img.width * 0.5), int(img.height * 0.5))
            resized_img = img.resize(new_size)
            resized_img.save(output_path, format="WEBP")

        destination_key = os.path.join(destination_prefix, output_file_name)
        with open(output_path, 'rb') as f:
            client.put_object(bucket_name, destination_key, content=f)

        print(f"Uploaded resized image to {destination_key}")
    except Exception as e:
        raise Exception(f"Error processing image: {e}")

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Image resized and converted to WebP successfully'})
    }