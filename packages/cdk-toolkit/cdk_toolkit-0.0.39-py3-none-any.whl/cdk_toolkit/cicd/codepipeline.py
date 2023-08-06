from aws_cdk import (  
    aws_codepipeline as codepipeline, 
) 
 

##
## CodePipeline
def createCodePipelineArtifact():
    artifact = codepipeline.Artifact()
    return artifact

def createCodePipeline(self, codepipeline_name, codepipeline_role, source_action, build_action, deploy_action=None):
    stages = []
    stages.append(codepipeline.StageProps(stage_name="Source", actions=[source_action]))
    stages.append(codepipeline.StageProps(stage_name="Build", actions=[build_action]))
    if deploy_action is not None:
        stages.append(codepipeline.StageProps(stage_name="Deploy", actions=[deploy_action]))

    pipeline = codepipeline.Pipeline(
        self, "CDK-CodePipeline-{}".format(codepipeline_name),
        pipeline_name="{}".format(codepipeline_name), 
        role=codepipeline_role,
        stages=stages,
    ) 
    return pipeline