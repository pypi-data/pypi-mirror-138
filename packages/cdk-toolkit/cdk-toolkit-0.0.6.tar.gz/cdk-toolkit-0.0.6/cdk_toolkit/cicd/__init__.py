from constructs import Construct
from aws_cdk import ( 
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild
)


##
## CodeCommit
def createCodeCommitRepository(self, repository_name):
    """
    Creates a CodeCommit Repository.
 
    :param repository_name: Name of the CodeCommit Repository
    :return: CodeCommit Repository Object
    """ 
    repo = codecommit.Repository(
        self, 'CDK-CodeCommit-Repository-{}'.format(repository_name),
        repository_name= repository_name
    )
    return repo

def existingCodeCommitRepository(self):
    return 

def createCodeCommitSourceAction(self, codecommit_repository, codecommit_repository_branch, codecommit_output_artifact):
    """
    Creates a CodeCommit Source Action.
 
    :param codecommit_repository: CodeCommit Repository Object
    :param codecommit_repository_branch: CodeCommit Repository Bran
    :param codecommit_output_artifact: CodeCommit Output Artifact
    :return: CodeCommit Source Action
    """ 
    codecommit_source_action = codepipeline_actions.CodeCommitSourceAction(
        action_name="Source", 
        repository=codecommit_repository,
        branch=codecommit_repository_branch, 
        output=codecommit_output_artifact 
    )  
    return codecommit_source_action


##
## CodeBuild
def createCodeBuildAction(self, codebuild_action_name, codebuild_input_artifact, codebuild_role):
    """
    Creates a CodeBuild Action.
 
    :param codebuild_action_name: Name of the CodeBuild Action
    :param codebuild_input_artifact: CodeBuild Input Artifact (Source Output)
    :param codebuild_role: IAM CodeBuild Role Object
    :return: CodeBuild Build Action
    """ 
    codebuild_build_action = codepipeline_actions.CodeBuildAction(
        action_name=codebuild_action_name,
        # Configure your project here
        project=codebuild.PipelineProject(
            self, codebuild_action_name,
            project_name=codebuild_action_name,
            role=codebuild_role,
            environment=codebuild.BuildEnvironment(
                privileged=True
            ), 
        ),
        input=codebuild_input_artifact,
    )
    return codebuild_build_action


##
## CodePipeline
def createCodePipelineArtifact():
    artifact = codepipeline.Artifact()
    return artifact

def createCodePipeline(self, codepipeline_name, source_action, build_action, deploy_action=None):
    stages = []
    stages.append(codepipeline.StageProps(stage_name="Source", actions=[source_action]))
    stages.append(codepipeline.StageProps(stage_name="Build", actions=[build_action]))
    if deploy_action is not None:
        stages.append(codepipeline.StageProps(stage_name="Deploy", actions=[deploy_action]))

    pipeline = codepipeline.Pipeline(
        self, "CDK-CodePipeline-{}".format(codepipeline_name),
        pipeline_name="{}".format(codepipeline_name), 
        stages=stages, 
    ) 
    return pipeline
