from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import cicd
from cdk_toolkit.cicd.codebuild import createCodeBuildEnvironmentVariable 


class ECRCodePipelineStack(Stack): 
    '''
    This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
    '''
    def __init__(self, scope: Construct, construct_id: str, codecommit_repository_name: str, codecommit_repository_branch: str, codebuild_action_name: str, codebuild_role: str, codepipeline_name: str, codecommit_initial_commit_dir: str, ecr_repository_name: str, ecr_repository_tag: str, ecr_account_id: str, ecr_account_region: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        # Create CodeCommit Repository 
        codecommit_repository = cicd.createCodeCommitRepository(self, codecommit_repository_name, initial_commit_dir=codecommit_initial_commit_dir, initial_commit_branch=codecommit_repository_branch)

        # Create CodeCommit Artifact
        codecommit_artifact = cicd.createCodePipelineArtifact()

        # Create CodeCommit Source Action
        codecommit_source_action = cicd.createCodeCommitSourceAction(self, codecommit_repository, codecommit_repository_branch, codecommit_artifact)

        # Create CodeBuild Build Action 
        codebuild_env_variables = {
                    "ECR_REPO_NAME": createCodeBuildEnvironmentVariable(self, ecr_repository_name),
                    "ECR_REPO_TAG": createCodeBuildEnvironmentVariable(self, ecr_repository_tag),
                    "AWS_ACCOUNT_ID": createCodeBuildEnvironmentVariable(self, ecr_account_id),
                    "AWS_ACCOUNT_REGION": createCodeBuildEnvironmentVariable(self, ecr_account_region)
                }
        codebuild_build_action = cicd.createCodeBuildAction(self, codebuild_action_name, codecommit_artifact, codebuild_role, codebuild_env_variables=None)

        # Create CodePipeline
        codepipeline = cicd.createCodePipeline(self, codepipeline_name, codecommit_source_action, codebuild_build_action, deploy_action=None)


        