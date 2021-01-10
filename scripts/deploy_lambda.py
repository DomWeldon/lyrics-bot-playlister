"""Look at terraform config to find branch specific environment vars"""
from os import environ
from pathlib import Path
from typing import Dict, List, NewType, Tuple

import boto3

AwsAccessKeyId = NewType("AwsAccessKeyId", str)
AwsRegionName = NewType("AwsRegionName", str)
AwsSecretAccessKey = NewType("AwsSecretAccessKey", str)
BranchName = NewType("BranchName", str)
EnvVarKey = NewType("EnvVarKey", str)
LambdaFunctionAlias = NewType("LambdaFunctionAlias", str)
LambdaFunctionVersion = NewType("LambdaFunctionVersion", str)
LambdaKey = NewType("LambdaKey", str)
PartialSsmParamName = NewType("PartialSsmParamName", str)
ProjectName = NewType("ProjectName", str)
RoleArn = NewType("RoleArn", str)
RoleSessionName = NewType("RoleSessionName", str)
SsmParamName = NewType("SsmParamName", str)
SsmParam = NewType("SsmParam", str)


def get_and_parse_ssm_params(
    ssm_client,
    project_name: ProjectName,
    branch_name: BranchName,
    param_names: List[SsmParamName],
) -> Dict[PartialSsmParamName, SsmParam]:
    """Return a dict of SSM params"""
    response = ssm_client.get_parameters(
        Names=[
            f"/{project_name}/{branch_name}{param_name}"
            for param_name in param_names
        ]
    )

    return {
        PartialSsmParamName(
            "/" + "/".join(param["Name"].split("/")[3:])
        ): SsmParam(param["Value"])
        for param in response["Parameters"]
    }


def get_branch_specific_arn(branch_name: BranchName) -> RoleArn:
    """Get the role ARN, specific to the branch."""
    role_arn_env_var = f"AWS_ROLE_ARN_{branch_name.upper()}"
    try:
        role_arn = environ[role_arn_env_var]
    except KeyError:
        raise Exception(
            f"No environment variable found at {role_arn_env_var} "
            f"for branch {branch_name}."
        )

    return RoleArn(role_arn)


def get_role_session_name() -> RoleSessionName:
    """Build a RoleSessionName from env vars."""
    # get arn and session name
    circle_sha1 = environ["CIRCLE_SHA1"]
    circle_build_num = environ["CIRCLE_BUILD_NUM"]
    role_session_name = f"{circle_sha1}-job={circle_build_num}"

    return role_session_name


# main functions coupled to CI
def deploy_lambda(
    ssm_client,
    lambda_client,
    s3_client,
    lambda_key: LambdaKey,
    project_name: ProjectName,
    branch_name: BranchName,
    our_lambda_ref: PartialSsmParamName,
    artefact: Path,
) -> Tuple[LambdaFunctionVersion, LambdaFunctionAlias]:
    """Deploy a lambda function, closely coupled to terraform/SSM."""
    # get the contents of the archive in bytes
    with artefact.open("rb") as _:
        contents = _.read()

    params = get_and_parse_ssm_params(
        ssm_client,
        project_name,
        branch_name,
        [
            f"/{our_lambda_ref}{key}"
            for key in {"/source/key", "/source/bucket_id", "/lambda/arn"}
        ],
    )

    s3_response = s3_client.put_object(
        Body=contents,
        Bucket=params[f"/{our_lambda_ref}/source/bucket_id"],
        Key=params[f"/{our_lambda_ref}/source/key"],
    )
    s3_version_id = s3_response["VersionId"]

    lambda_response = lambda_client.update_function_code(
        FunctionName=params[f"/{our_lambda_ref}/lambda/arn"],
        S3Bucket=params[f"/{our_lambda_ref}/source/bucket_id"],
        S3Key=params[f"/{our_lambda_ref}/source/key"],
        S3ObjectVersion=s3_version_id,
        Publish=True,
    )
    print(f"Published version {lambda_response['Version']}")


def main() -> None:
    """Deploy the lambda function."""
    # get relevant role ARN for this environment (dev/prod) from envvars
    lambda_key = ProjectName(environ["LAMBDA_KEY"])
    project_name = ProjectName(environ["PROJECT_NAME"])
    branch_name = BranchName(environ["CIRCLE_BRANCH"])
    role_arn = get_branch_specific_arn(branch_name)
    role_session_name = get_role_session_name()

    # get the CI user for all environments from envvars
    aws_region_name = AwsRegionName(environ["AWS_REGION"])
    aws_access_key_id = AwsAccessKeyId(environ["AWS_ACCESS_KEY_ID"])
    aws_secret_access_key = AwsSecretAccessKey(
        environ["AWS_SECRET_ACCESS_KEY"]
    )

    # get STS client to assume the role
    client = boto3.client(
        "sts",
        region_name=aws_region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # make a request for a token and assume this role from here on in
    response = client.assume_role(
        RoleArn=role_arn, RoleSessionName=role_session_name
    )

    # store the credentials to use later
    credentials = response["Credentials"]
    credentials_key_map = {
        "aws_secret_access_key": "SecretAccessKey",
        "aws_access_key_id": "AccessKeyId",
        "aws_session_token": "SessionToken",
    }
    credentials_values = {
        k: credentials[v] for k, v in credentials_key_map.items()
    }

    # Now pull relevant ARNs out of Lambda
    # get the ssm client
    ssm_client = boto3.client(
        "ssm", region_name=aws_region_name, **credentials_values
    )

    # Deploy our lambda
    s3_client = boto3.client(
        "s3", region_name=aws_region_name, **credentials_values
    )
    lambda_client = boto3.client(
        "lambda", region_name=aws_region_name, **credentials_values
    )

    print("Deploying Lambda")
    deploy_lambda(
        ssm_client,
        lambda_client,
        s3_client,
        lambda_key,
        project_name,
        branch_name,
        PartialSsmParamName(lambda_key),
        Path("./artefact.zip"),
    )


if __name__ == "__main__":
    main()
