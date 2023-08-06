from aws_cdk import Stack 
from constructs import Construct

from cdk_toolkit import connection, container


# class EKSStack(Stack): 
#     '''
#     This Stack Creates a CodePipeline that Updates ECR Images when a given CodeCommit Repository is Updated
#     '''
#     def __init__(self, scope: Construct, construct_id: str, eks_cluster_name: str, vpc: ec2.Vpc, eks_role: iam.Role, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         eks_role = iam.Role(self, "eksadmin", assumed_by=iam.ServicePrincipal(service='ec2.amazonaws.com'),
#                             role_name='eks-cluster-role', managed_policies=
#                             [iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AdministratorAccess')])
#         eks_instance_profile = iam.CfnInstanceProfile(self, 'instanceprofile',
#                                                       roles=[eks_role.role_name],
#                                                       instance_profile_name='eks-cluster-role')

#         cluster = eks.Cluster(self, 'data-lake-eks-cluster', cluster_name=eks_cluster_name,
#                               version=eks.KubernetesVersion.V1_21,
#                               vpc=vpc,
#                               vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)],
#                               default_capacity=0,
#                               masters_role=eks_role)

#         nodegroup = cluster.add_nodegroup_capacity('eks-nodegroup',
#                                                    instance_types=[ec2.InstanceType('t3.large'),
#                                                                    ec2.InstanceType('m5.large'),
#                                                                    ec2.InstanceType('c5.large')],
#                                                    disk_size=50,
#                                                    min_size=2,
#                                                    max_size=2,
#                                                    desired_size=2,
#                                                    subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
#                                                    remote_access=eks.NodegroupRemoteAccess(
#                                                        ssh_key_name='ie-prod-snow-common'),
#                                                    capacity_type=eks.CapacityType.SPOT)
