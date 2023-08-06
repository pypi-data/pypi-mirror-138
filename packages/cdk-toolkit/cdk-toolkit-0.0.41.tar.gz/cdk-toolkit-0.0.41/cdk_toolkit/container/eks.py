from aws_cdk import ( 
    aws_eks as eks,
    aws_ec2 as ec2
) 


##
## EKS
def createEKS_EC2Cluster(self, eks_cluster_name, eks_role, vpc): 
    eks_cluster = eks.Cluster(self, 'data-lake-eks-cluster', cluster_name=eks_cluster_name,
                              version=eks.KubernetesVersion.V1_21,
                              vpc=vpc,
                              vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)],
                              default_capacity=0,
                              masters_role=eks_role) 
    return eks_cluster

def createEKS_FargateCluster(self, eks_cluster_name, eks_role, vpc): 
    eks_cluster = eks.FargateCluster(self, "fargate-eks-cluster", 
                                cluster_name=eks_cluster_name,
                                version=eks.KubernetesVersion.V1_21,
                                masters_role=eks_role, 
    ) 
    return eks_cluster


def addEKS_EC2ClusterNodeGroup(self, eks_cluster):
    nodegroup = eks_cluster.add_nodegroup_capacity('eks-nodegroup',
                    instance_types=[ec2.InstanceType('t3.large'),
                                    ec2.InstanceType('m5.large'),
                                    ec2.InstanceType('c5.large')],
                    disk_size=50,
                    min_size=2,
                    max_size=2,
                    desired_size=2,
                    subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                    # remote_access=eks.NodegroupRemoteAccess(ssh_key_name='ie-prod-snow-common'),
                    capacity_type=eks.CapacityType.SPOT)

def applyEKSManifest(self, eks_cluster):
    eks_cluster.add_manifest("mypod", {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": { "name": "mypod" },
        "spec": {
                "containers": [
                    {
                        "name": "hello",
                        "image": "amazon/amazon-ecs-sample",
                        "ports": [{ "containerPort": 8080 }],
                    }
                ]
            }
        }
    )