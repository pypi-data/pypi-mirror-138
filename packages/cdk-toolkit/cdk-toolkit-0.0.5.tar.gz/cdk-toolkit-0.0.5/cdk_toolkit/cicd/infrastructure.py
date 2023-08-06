from constructs import Construct
from aws_cdk import Stack, Aws
import aws_cdk as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_codecommit as codecommit



def existingCodeCommitRepo(self, repository_name):
    repository = codecommit.Repository(self, "Repo", repository_name=repository_name)
    return repository