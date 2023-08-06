import os, json
from cdk_toolkit.permission.iam import *


def readIAMRolePolicyStatements(roles_dir, role_name):
    json_file_path = os.path.join(roles_dir, "{}.json".format(role_name))  
    with open(json_file_path) as json_file:
        role_json = json.load(json_file)
    return role_json