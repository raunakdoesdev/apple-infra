from abc import ABC
from typing import Optional

import boto3
from arcadia_typedefs import LocalFile
from botocore.client import BaseClient

from aml_ingestion_common.provider import CachingClientProvider, T


class AWSClientProvider(CachingClientProvider[BaseClient], ABC):

    def __init__(self, ttl: Optional[int], region_name: Optional[str] = None):
        super().__init__(ttl)
        self._region = region_name


class AWSLocalClientProvider(AWSClientProvider):

    def __init__(self, profile_name: str, region_name: Optional[str] = None):
        super().__init__(ttl=None, region_name=region_name)  # Cache always
        self.__profile = profile_name

    def _instantiate(self, client_id: str) -> BaseClient:
        session = boto3.Session(profile_name=self.__profile, region_name=self._region)
        return session.client(client_id)

class AWSVirtualMacClientProvider(AWSClientProvider):

    def __init__(self):
        super().__init__(ttl=None, region_name=None)

    def _instantiate(self, client_id: str) -> BaseClient:
        return boto3.client(client_id)

class EKSClientProvider(AWSClientProvider):

    def __init__(self,
                 role_arn: str,
                 token_file_path: str,
                 ttl: int = 0,  # Does not cache by default
                 region_name: Optional[str] = None,
                 **role_mapping: str
                 ):
        super().__init__(ttl, region_name)
        self.__role_arn = role_arn
        self.__token_file = LocalFile(token_file_path)
        self.__roles = role_mapping

    def __get_sts_assume_role_credentials(self, client_id: str):
        """
        - Read web_identity_token from given token file path
        - Use sts_connection to assume IAM role with web_identity_token
        - Return credentials corresponding to assumed role
        """

        sts_connection = boto3.client('sts')
        web_identity_token = self.__token_file.read().strip()
        assume_role_object = sts_connection.assume_role_with_web_identity(
            RoleArn=self.__role_arn,
            RoleSessionName=self.__roles[client_id],
            WebIdentityToken=web_identity_token
        )
        return assume_role_object['Credentials']

    def _instantiate(self, client_id: str) -> BaseClient:
        credentials = self.__get_sts_assume_role_credentials(client_id)
        return boto3.client(
            client_id,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=self._region)


# vim: set ft=python nospell syntax=python nowrap tabstop=4 expandtab shiftwidth=4 softtabstop=4:
