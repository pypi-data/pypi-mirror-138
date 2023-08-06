from aws_cdk import ( 
    aws_codecommit as codecommit, 
    aws_codepipeline_actions as codepipeline_actions, 
) 



##
## CodeCommit
def createCodeCommitRepository(self, repository_name, initial_commit=None):
    """
    Creates a CodeCommit Repository.
 
    :param repository_name: Name of the CodeCommit Repository
    :param initial_commit: CodeCommit Repository Initial Commit (defaul=None)
    :return: CodeCommit Repository Object
    """ 
    repo = codecommit.Repository(
        self, 'CDK-CodeCommit-Repository-{}'.format(repository_name),
        repository_name= repository_name,
        code=initial_commit
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