from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import permission 
from cdk_toolkit.permission import readIAMRolePolicyStatements


class IAMRolesStack(Stack): 
    '''
    This Stack Creates all the necessary IAM roles for other Toolkit Stacks
    '''
    def __init__(self, scope: Construct, construct_id: str, iam_roles_dir: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##
        ## CodeBuild Service Role
        codebuild_svc_role_dictionary = readIAMRolePolicyStatements(iam_roles_dir, "codebuild_svc_role")
        self.codebuild_svc_role = permission.createIAMServiceRole(self, codebuild_svc_role_dictionary)






