from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import connection 


class VPCStack(Stack): 
    '''
    This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
    '''
    def __init__(self, scope: Construct, construct_id: str, vpc_name: str, cidr_str: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        ## 
        ## VPC 
        ################################
        stack_env_name = self.node.try_get_context("env")
        self.vpc = connection.createVPC(self, vpc_name, cidr_str, stack_env_name)
        