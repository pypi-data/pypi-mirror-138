from aws_cdk import ( 
    aws_ssm as ssm
) 


##
## SSM
def createSSMStringParameter(self, ssm_name, string_value, parameter_name): 
    ssm.StringParameter(self, ssm_name, string_value = string_value, parameter_name = parameter_name)
