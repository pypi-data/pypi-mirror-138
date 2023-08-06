from aws_cdk import Stack
from aws_cdk import (
    aws_ssm as ssm,
    aws_ec2 as ec2
)
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
        # stack_env_name = "cdktoolkit" #self.node.try_get_context("env")
        # self.vpc = connection.createVPC(self, vpc_name, cidr_str, stack_env_name)

        # priv_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]
        # count = 1
        # for ps in priv_subnets: 
        #     aws_ssm.StringParameter(self, 'private-subnet-'+ str(count),
        #         string_value = ps,
        #         parameter_name = '/'+stack_env_name+'/private-subnet-'+str(count)
        #         )
        #     count += 1  
        # The code that defines your stack goes here
        env_name = self.node.try_get_context("env")

        self.vpc = ec2.Vpc(self, 'data-lake-vpc',
            vpc_name = vpc_name,
            cidr = cidr_str,
            max_azs = 2,
            enable_dns_hostnames = True, 
            enable_dns_support = True, 
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name = 'Public-Subent',
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 26
                ),
                ec2.SubnetConfiguration(
                    name = 'Private-Subnet',
                    subnet_type = ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask = 26
                )
            ],
            nat_gateways = 1,
            

        )
        priv_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        count = 1
        for ps in priv_subnets: 
            ssm.StringParameter(self, 'private-subnet-'+ str(count),
                string_value = ps,
                parameter_name = '/'+env_name+'/private-subnet-'+str(count)
                )
            count += 1  
         