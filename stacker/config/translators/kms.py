import base64
import botocore.session


def kms_simple_decrypt(value):
    """Decrypt the specified value with a master key in KMS.

    kmssimple field types should be in the following format:

        [<region>@]<base64 encrypted value>

    Note: The region is optional, and defaults to us-east-1 if not given.

    For example:

        # We use the aws cli to get the encrypted value for the string
        # "PASSWORD" using the master key called 'myStackerKey' in us-east-1
        $ aws --region us-east-1 kms encrypt --key-id alias/myStackerKey \
                --plaintext "PASSWORD" --output text --query CiphertextBlob

        CiD6bC8t2Y<...encrypted blob...>

        # In stacker we would reference the encrypted value like:
        conf_key: !kms us-east-1@CiD6bC8t2Y<...encrypted blob...>

        # The above would resolve to
        conf_key: PASSWORD
    """
    region = 'us-east-1'
    if '@' in value:
        region, value = value.split('@', 1)

    s = botocore.session.get_session()
    kms = s.create_client('kms', region_name=region)
    decoded = base64.b64decode(value)
    response = kms.decrypt(CiphertextBlob=decoded)
    return response["Plaintext"]


def kms_simple_constructor(loader, node):
    value = loader.construct_scalar(node)
    return kms_simple_decrypt(value)
