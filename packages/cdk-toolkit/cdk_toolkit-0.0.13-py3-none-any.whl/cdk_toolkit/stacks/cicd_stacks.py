from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import cicd 


class CDKCodePipelineStack(Stack): 
    def __init__(self, scope: Construct, construct_id: str, codecommit_repository_name: str, codecommit_repository_branch: str, codebuild_action_name: str, codebuild_role: str, codepipeline_name: str, codecommit_initial_commit_dir: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create CodeCommit Repository 
        codecommit_repository = cicd.createCodeCommitRepository(self, codecommit_repository_name, initial_commit_dir=codecommit_initial_commit_dir, initial_commit_branch="main")

        # Create CodeCommit Artifact
        codecommit_artifact = cicd.createCodePipelineArtifact()

        # Create CodeCommit Source Action
        codecommit_source_action = cicd.createCodeCommitSourceAction(self, codecommit_repository, codecommit_repository_branch, codecommit_artifact)

        # Create CodeBuild Build Action
        codebuild_buildspec = ''
        codebuild_build_action = cicd.createCodeBuildAction(self, codebuild_action_name, codecommit_artifact, codebuild_role)

        # Create CodePipeline
        codepipeline = cicd.createCodePipeline(self, codepipeline_name, codecommit_source_action, codebuild_build_action, deploy_action=None)


        