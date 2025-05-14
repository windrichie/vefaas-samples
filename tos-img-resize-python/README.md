# BytePlus TOS Image Resizer

This repository contains a serverless function that automatically resizes images and converts them to WebP format when they are uploaded to a BytePlus Torch Object Storage (TOS) bucket.

## Architecture

- Images uploaded to a TOS bucket under the `original/` folder trigger the function
- The function downloads the image, resizes it to 50% of original dimensions, and converts it to WebP format
- The processed image is uploaded back to the same bucket under the `resized/` folder

## Repository Contents

- `index.py` - Source code for the image processing function
- `requirements.txt` - Python dependencies (Pillow and TOS SDK)

## Quick Start

1. Create a TOS bucket in your BytePlus account
2. Create two folders in the bucket: `original/` and `resized/`
3. Create an IAM user with read/write access to your TOS bucket
4. Deploy a Python function using the code in this repository
5. Configure a TOS trigger for the function:
   - Event type: `tos:ObjectCreated:*`
   - Prefix filter: `original/`
6. Upload an image to the `original/` folder and observe the resized version appear in `resized/`

## Prerequisites

- BytePlus account with access to Function Service and TOS
- IAM user with appropriate permissions for TOS access