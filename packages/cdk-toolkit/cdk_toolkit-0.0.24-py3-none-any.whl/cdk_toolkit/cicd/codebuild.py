from aws_cdk import (  
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild
) 


##
## CodeBuild
def createCodeBuildAction(self, codebuild_action_name, codebuild_input_artifact, codebuild_role, codebuild_env_variables=None):
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
            environment_variables=codebuild_env_variables
            
        ),
        input=codebuild_input_artifact,
    )
    return codebuild_build_action

def createCodeBuildEnvironmentVariable(self, env_var_value):
    return codebuild.BuildEnvironmentVariable(value=env_var_value)