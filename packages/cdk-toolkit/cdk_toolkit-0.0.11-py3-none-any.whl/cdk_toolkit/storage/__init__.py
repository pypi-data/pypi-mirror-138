from constructs import Construct
from aws_cdk import (
    Aws, 
    RemovalPolicy, 
    aws_s3 as s3, 
)

##
## S3 Buckets
def createS3Bucket(self, bucket_name, versioned=False): 
    """
    Creates an S3 Bucket.
 
    :param bucket_name: Name of the S3 Bucket
    :param versioned: Enable Bucket Versioning (default=False)
    :return: S3 Bucket Object
    """ 
    bucket = s3.Bucket(
        self, "DataLakeS3Bucket",
        bucket_name=bucket_name,
        versioned=versioned,
        removal_policy=RemovalPolicy.DESTROY
    )
    return bucket

def existingS3Bucket():
    return 


##
## EFS


##
## EBS