from aws_cdk import ( 
     aws_ec2 as ec2, 
     aws_ssm as ssm
) 


def createVPC(self, vpc_name, cidr_str, stack_env_name):
    vpc = ec2.Vpc(self, vpc_name,
        vpc_name = vpc_name,
        cidr = cidr_str,
        max_azs = 2,
        enable_dns_hostnames = True, 
        enable_dns_support = True, 
        subnet_configuration=[
            ec2.SubnetConfiguration(
                name = 'Public-Subent',
                subnet_type = ec2.SubnetType.PUBLIC,
                cidr_mask = 26
            ),
            ec2.SubnetConfiguration(
                name = 'Private-Subnet',
                subnet_type = ec2.SubnetType.PRIVATE_ISOLATED,
                cidr_mask = 26
            )
        ],
        # nat_gateways = 1,
        

    )
    # priv_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]

    # count = 1
    # for ps in priv_subnets: 
    #     ssm.StringParameter(self, 'private-subnet-'+ str(count),
    #         string_value = ps,
    #         parameter_name = '/'+stack_env_name+'/private-subnet-'+str(count)
    #         )
    #     count += 1 
    return vpc