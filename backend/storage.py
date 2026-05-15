import boto3
from botocore.exceptions import ClientError
from backend.config import settings

import os
from pathlib import Path

class R2Storage:
    def __init__(self):
        self.is_local = not settings.R2_ENDPOINT
        if self.is_local:
            print("⚠️ R2_ENDPOINT not set. Falling back to local storage.")
            self.local_path = Path("storage")
            self.local_path.mkdir(exist_ok=True)
            self.s3_client = None
        else:
            self.s3_client = boto3.client(
                "s3",
                endpoint_url=settings.R2_ENDPOINT,
                aws_access_key_id=settings.R2_ACCESS_KEY,
                aws_secret_access_key=settings.R2_SECRET_KEY,
                region_name="auto",
            )
        self.bucket_name = settings.R2_BUCKET

    def upload_file(self, file_bytes: bytes, key: str) -> str:
        if self.is_local:
            file_path = self.local_path / key
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(file_bytes)
            return key
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_bytes,
                ContentType="application/pdf"
            )
            return key
        except ClientError as e:
            print(f"Error uploading to R2: {e}")
            raise e

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        if self.is_local:
            # In local mode, we just return a "file://" style path or a placeholder
            return f"file:///{os.path.abspath(self.local_path / key)}"
            
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expires_in,
            )
            return url
        except ClientError as e:
            print(f"Error generating pre-signed URL: {e}")
            raise e

    def get_file(self, key: str) -> bytes:
        if self.is_local:
            file_path = self.local_path / key
            with open(file_path, "rb") as f:
                return f.read()
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read()
        except ClientError as e:
            print(f"Error fetching from R2: {e}")
            raise e

    def delete_file(self, key: str):
        if self.is_local:
            file_path = self.local_path / key
            if file_path.exists():
                file_path.unlink()
            return
            
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            print(f"Error deleting from R2: {e}")
            raise e

storage = R2Storage()
