from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import cicd, container, permission
from cdk_toolkit.cicd.codebuild import createCodeBuildEnvironmentVariable 


class ECRCodePipelineStack(Stack): 
    '''
    This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
    '''
    def __init__(self, scope: Construct, construct_id: str, codecommit_repository_name: str, codecommit_repository_branch: str, codebuild_action_name: str, codebuild_role_arn: permission.iam.Role.role_arn, codepipeline_name: str, codepipeline_role_arn: permission.iam.Role.role_arn, codecommit_initial_commit_dir: str, ecr_repository_name: str, ecr_repository_tag: str, ecr_account_id: str, ecr_account_region: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        ## 
        ## ECR 
        ################################

        ## Create ECR Repository
        ecr_repository = container.createECRRepository(self, ecr_repository_name)




        ## 
        ## CodeCommit
        ################################
        
        ## Create CodeCommit Repository 
        codecommit_repository = cicd.createCodeCommitRepository(self, codecommit_repository_name, initial_commit_dir=codecommit_initial_commit_dir, initial_commit_branch=codecommit_repository_branch)
 
        ## Create CodeCommit Artifact
        codecommit_artifact = cicd.createCodePipelineArtifact()

        ## Create CodeCommit Source Action
        codecommit_source_action = cicd.createCodeCommitSourceAction(self, codecommit_repository, codecommit_repository_branch, codecommit_artifact)




        ## 
        ## CodeBuild
        ################################
        ## Attach CodeBuild Service Role
        codebuild_svc_role =  permission.iam.Role.from_role_arn(
            self, "codebuild_svc_role",
            role_arn=codebuild_role_arn
        )

        ## Create CodeBuild Build Environment Variables
        codebuild_env_variables = {
                    "ECR_REPO_NAME": createCodeBuildEnvironmentVariable(self, ecr_repository.repository_name),
                    "ECR_REPO_TAG": createCodeBuildEnvironmentVariable(self, ecr_repository_tag),
                    "AWS_ACCOUNT_ID": createCodeBuildEnvironmentVariable(self, ecr_account_id),
                    "AWS_ACCOUNT_REGION": createCodeBuildEnvironmentVariable(self, ecr_account_region)
                }

        # Create CodeBuild Build Action
        codebuild_build_action = cicd.createCodeBuildAction(self, codebuild_action_name, codecommit_artifact, codebuild_svc_role, codebuild_env_variables=codebuild_env_variables)




        ## 
        ## CodePipeline
        ################################
        ## Attach CodePipeline Service Role
        codebuild_svc_role =  permission.iam.Role.from_role_arn(
            self, "codepipeline_svc_role",
            role_arn=codepipeline_role_arn
        )
        # Create CodePipeline
        codepipeline = cicd.createCodePipeline(self, codepipeline_name, codebuild_svc_role, codecommit_source_action, codebuild_build_action, deploy_action=None)


        