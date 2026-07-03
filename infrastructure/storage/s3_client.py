from typing import Optional

import boto3
from botocore.client import Config


class S3Client:
    def __init__(
        self,
        bucket_name: str,
        access_key: str,
        secret_key: str,
        region: str = "us-east-1",
    ) -> None:
        self._bucket_name = bucket_name
        self._client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            config=Config(signature_version="s3v4"),
        )

    async def upload_file(
        self,
        key: str,
        content: bytes,
        content_type: str,
    ) -> str:
        """Upload a file to S3."""
        self._client.put_object(
            Bucket=self._bucket_name,
            Key=key,
            Body=content,
            ContentType=content_type,
        )
        return f"s3://{self._bucket_name}/{key}"

    async def download_file(self, key: str) -> bytes:
        """Download a file from S3."""
        response = self._client.get_object(Bucket=self._bucket_name, Key=key)
        return response["Body"].read()

    async def delete_file(self, key: str) -> None:
        """Delete a file from S3."""
        self._client.delete_object(Bucket=self._bucket_name, Key=key)

    async def generate_presigned_url(
        self,
        key: str,
        expiration: int = 3600,
    ) -> str:
        """Generate a presigned URL for a file."""
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket_name, "Key": key},
            ExpiresIn=expiration,
        )
