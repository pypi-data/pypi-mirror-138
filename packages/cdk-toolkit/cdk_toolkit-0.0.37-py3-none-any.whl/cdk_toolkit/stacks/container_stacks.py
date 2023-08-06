from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import connection, container, permission


class EKSStack(Stack): 
    '''
    This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
    '''
    def __init__(self, scope: Construct, construct_id: str, eks_cluster_name: str, eks_role_arn: str, vpc: connection.ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        eks_role =  permission.iam.Role.from_role_arn(self, "eks_admin_role", role_arn=eks_role_arn)
        # eks_instance_profile = iam.CfnInstanceProfile(self, 'instanceprofile',
        #                                               roles=[eks_role.role_name],
        #                                               instance_profile_name='eks-cluster-role')
        
        cluster = container.createEKSCluster(self, eks_cluster_name, eks_role)
        nodegroup = container.addEKSClusterNodeGroup(self, cluster) 
