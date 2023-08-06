from aws_cdk import Stack, aws_ssm
from constructs import Construct

from cdk_toolkit import connection, container


class VPCStack(Stack): 
    '''
    This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
    '''
    def __init__(self, scope: Construct, construct_id: str, vpc_name: str, cidr_str: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        ## 
        ## VPC 
        ################################
        stack_env_name = "cdktoolkit" #self.node.try_get_context("env")
        self.vpc = connection.createVPC(self, vpc_name, cidr_str, stack_env_name)

        priv_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]
        count = 1
        for ps in priv_subnets: 
            aws_ssm.StringParameter(self, 'private-subnet-'+ str(count),
                string_value = ps,
                parameter_name = '/'+stack_env_name+'/private-subnet-'+str(count)
                )
            count += 1  
         