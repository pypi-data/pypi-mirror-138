from aws_cdk import ( 
    aws_iam as iam
)  


##
## IAM
def createIAMServiceRole(self, svc_role_dictionary): 
    svc_role_name = svc_role_dictionary["service_role_name"]
    svc_role_description = svc_role_dictionary["service_role_description"]
    svc_role_principal = svc_role_dictionary["service_role_principal"]
    svc_role_permissions = svc_role_dictionary["service_role_permissions"]
    role = iam.Role(self, svc_role_name,
        assumed_by=iam.ServicePrincipal(svc_role_principal),
        role_name=svc_role_name,
        description=svc_role_description
    )
    for policy_statement in svc_role_permissions:
        policy_sid = policy_statement["Sid"]
        policy_effect = policy_statement["Effect"]
        policy_actions = policy_statement["Action"]
        policy_resources = policy_statement["Resource"]
        if policy_effect == "Allow":
            policy_effect = iam.Effect.ALLOW
        if policy_effect == "Deny":
            policy_effect = iam.Effect.DENY
        role.add_to_policy(iam.PolicyStatement(
                sid=policy_sid,
                effect=policy_effect,
                resources=policy_resources,
                actions=policy_actions
            ))
    return role

def createIAMManagedRole(self, managed_role_dictionary):
    managed_policies = []
    managed_role_name = managed_role_dictionary["managed_role_name"]
    managed_role_description = managed_role_dictionary["managed_role_description"]
    managed_role_principal = managed_role_dictionary["managed_role_principal"]
    managed_policy_names = managed_role_dictionary["managed_policy_names"]
    for managed_policy_name in managed_policy_names: 
        managed_policies.append(iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=managed_policy_name))
    role = iam.Role(self, managed_role_name,
        assumed_by=iam.ServicePrincipal(managed_role_principal),
        role_name=managed_role_name,
        description=managed_role_description,
        managed_policies=managed_policies
    )
    return role