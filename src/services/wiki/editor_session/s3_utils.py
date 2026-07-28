
import aioboto3

from src.core.settings import settings

s3_session = aioboto3.Session()


def get_s3_client():
    return s3_session.client(
        "s3",
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region_name,
    )


async def generate_presigned_get_url(key: str, expires_in: int = 3600) -> str:
    """ Link for reading files from s3 """
    async with get_s3_client() as s3:
        return await s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": settings.s3_bucket, "Key": key},
            ExpiresIn=expires_in,
        )


async def generate_presigned_put_url(
        key: str,
        content_type: str,
        expires_in: int = 3600,
) -> str:
    """ Link for uploading files to s3 """
    async with get_s3_client() as s3:
        return await s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.s3_bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )


async def delete_objects(keys: list[str]) -> None:
    """ Deleting objects from S3 (used to clean up orphaned media) """
    if not keys:
        return

    async with get_s3_client() as s3:
        await s3.delete_objects(
            Bucket=settings.s3_bucket,
            Delete={"Objects": [{"Key": key} for key in keys]},
        )

