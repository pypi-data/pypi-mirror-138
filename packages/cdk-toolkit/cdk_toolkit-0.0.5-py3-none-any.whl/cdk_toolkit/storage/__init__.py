print("AWS CDK TOOLKIT - STORAGE")


from constructs import Construct
from aws_cdk import (
    Aws, 
    RemovalPolicy, 
    aws_s3 as s3, 
)



def createS3Bucket(self, bucket_name, versioned=False): 
    bucket = s3.Bucket(
        self, "DataLakeS3Bucket",
        bucket_name=bucket_name,
        versioned=versioned,
        removal_policy=RemovalPolicy.DESTROY
    )
    return bucket

def existingS3Bucket():
    return 