from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import permission 


class IAMRolesStack(Stack): 
    '''
    This Stack Creates all the necessary IAM roles for other Toolkit Stacks
    '''
    def __init__(self, scope: Construct, construct_id: str, codecommit_repository_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)