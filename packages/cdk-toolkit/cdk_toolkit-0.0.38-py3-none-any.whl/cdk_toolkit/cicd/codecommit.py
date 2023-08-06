from aws_cdk import ( 
    aws_codecommit as codecommit, 
    aws_codepipeline_actions as codepipeline_actions, 
) 



##
## CodeCommit
def createCodeCommitRepository(self, repository_name, initial_commit_dir=None, initial_commit_branch=None):
    """
    Creates a CodeCommit Repository.
 
    :param repository_name: Name of the CodeCommit Repository
    :param initial_commit: CodeCommit Repository Initial Commit (defaul=None)
    :return: CodeCommit Repository Object
    """ 
    code = None
    commit_branch = "main"
    if initial_commit_branch is None:
        commit_branch = initial_commit_branch
    if initial_commit_dir is not None:
        code = codecommit.Code.from_directory(initial_commit_dir, commit_branch)
    repo = codecommit.Repository(
        self, 'CDK-CodeCommit-Repository-{}'.format(repository_name),
        repository_name= repository_name,
        code=code
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