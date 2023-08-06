from aws_cdk import ( 
    aws_ecr as ecr
) 


##
## EKS
def createEKSCluster(self, ecr_repository_name): 
    ecr_repo = ecr.Repository(self, ecr_repository_name, repository_name=ecr_repository_name, image_scan_on_push=True)
    return ecr_repo