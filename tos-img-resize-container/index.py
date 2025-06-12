import os
import json
import tempfile
from flask import Flask, request, jsonify
from PIL import Image
import tos

app = Flask(__name__)

# Replace with your IAM user credentials and endpoint
ak = ""
sk = "=="
endpoint = "tos-ap-southeast-1.ibytepluses.com"
region = "ap-southeast-1"
destination_prefix = "resized"

@app.route('/', methods=['POST'])
def process_image():
    print("Headers:", dict(request.headers))
    print("Body:", request.data.decode())

    try:
        print('v3')
        # Handle both JSON and octet-stream
        if request.is_json:
            data = request.get_json()
        elif request.headers.get('Content-Type') == 'application/octet-stream':
            data = json.loads(request.data.decode())
        else:
            return jsonify({"error": "Unsupported Content-Type"}), 415

        event = data["events"][0]
        object_key = event["tos"]["object"]["key"]
        bucket_name = event["tos"]["bucket"]["name"]
        base_file_name = os.path.basename(object_key)
        name, ext = os.path.splitext(base_file_name)

        if ext.lower() not in [".jpg", ".jpeg", ".png"]:
            return jsonify({"error": f"Unsupported file type: {ext}"}), 400

        if object_key.startswith(destination_prefix):
            return jsonify({"message": "Already processed, skipping."}), 200

        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, base_file_name)
            output_file_name = f"{name}.webp"
            output_path = os.path.join(temp_dir, output_file_name)

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

        return jsonify({"message": "Image resized and converted to WebP successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
