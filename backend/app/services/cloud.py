from repository.cloud import S3CloudRepository


class CloudService:
    def __init__(
        self,
        type: str,
        bucket_name: str,
        **kwargs,
    ):
        """
        Initialize the cloud service for the given bucket.
        """
        self.bucket_name = bucket_name
        if type == "s3":
            self.cloud_repository = S3CloudRepository(
                region_name=kwargs.get("region_name", "us-east-1"),
                access_key=kwargs.get("access_key", ""),
                secret_key=kwargs.get("secret_key", ""),
            )
        else:
            raise Exception("Invalid cloud service type")

    def upload_fileobj(
        self,
        object_name: str,
        file_path: str,
    ) -> bool:
        """
        Upload a file to the cloud.
        """
        return self.cloud_repository.upload_fileobj(
            bucket_name=self.bucket_name,
            object_name=object_name,
            file=file_path,
        )
