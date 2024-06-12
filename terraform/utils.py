"""Provides static access to AWS utilities and client providers
   configured via the environment"""

import os
from functools import lru_cache
from typing import NamedTuple, Optional

from aml_ingestion_common.aws.provider import (AWSClientProvider, AWSLocalClientProvider, AWSVirtualMacClientProvider,
                                               EKSClientProvider)


class S3File(NamedTuple):
    url: str
    bucket: str
    file_path: str
    base_name: str


def _get_from_environment(var_name: str,
                          default_value: Optional[str] = None,
                          required=False):
    value = os.getenv(var_name, default_value)
    if not value and required:
        raise RuntimeError(f'Expected {var_name} to be set in the environment')
    return value


class AWSClients:

    @staticmethod
    @lru_cache(maxsize=1)
    def _provider() -> AWSClientProvider:
        if _get_from_environment('DEPLOYMENT_ENV') == 'LOCAL':
            return AWSLocalClientProvider(
                profile_name=_get_from_environment('AWS_PROFILE_NAME', required=True),
                region_name=_get_from_environment('AWS_REGION', default_value='us-west-2'))
        elif _get_from_environment('DEPLOYMENT_ENV') == 'MACVM':
            return AWSVirtualMacClientProvider()
        return EKSClientProvider(
            role_arn=_get_from_environment('AWS_ROLE_ARN', required=True),
            token_file_path=_get_from_environment('AWS_WEB_IDENTITY_TOKEN_FILE', required=True),
            region_name=_get_from_environment('AWS_REGION', default_value='us-west-2'),
            ttl=int(_get_from_environment('AWS_CLIENT_TTL', default_value='0')),
            s3=_get_from_environment('AWS_S3_ROLE_SESSION_NAME', default_value='parsing_svc_s3_ops'),
            textract=_get_from_environment(
                'AWS_TEXTRACT_ROLE_SESSION_NAME', default_value='parsing_svc_textract_ops'))

    @classmethod
    def s3(cls):
        return cls._provider().get('s3')

    @classmethod
    def textract(cls):
        return cls._provider().get('textract')

    @classmethod
    def get(cls, client_id: str):
        return cls._provider().get(client_id)


class S3:

    @classmethod
    def __decode_if_needed(cls, location: S3File | str) -> S3File:
        return location if isinstance(location, S3File) else cls.decode_file_location(location)

    @staticmethod
    def decode_file_location(url: str) -> S3File:
        input_file_path = url[len('s3://'):]
        return S3File(
            url=url, bucket=input_file_path[:input_file_path.find('/')],
            file_path=input_file_path[input_file_path.find('/') + 1:],
            base_name=input_file_path[input_file_path.rfind('/') + 1:])

    @classmethod
    def read_file(cls, location: S3File | str) -> bytes:
        s3_file = cls.__decode_if_needed(location)
        s3_document = AWSClients.s3().get_object(Bucket=s3_file.bucket, Key=s3_file.file_path)
        return s3_document['Body'].read()

    @classmethod
    def write_file(cls, location: S3File | str, content: str):
        s3_file = cls.__decode_if_needed(location)
        AWSClients.s3().put_object(Body=content, Bucket=s3_file.bucket, Key=s3_file.file_path)

    @classmethod
    def delete_file(cls, location: S3File | str):
        s3_file = cls.__decode_if_needed(location)
        AWSClients.s3().delete_object(Bucket=s3_file.bucket, Key=s3_file.file_path)

    @classmethod
    def download_file(cls, location: S3File | str, local_path: str):
        s3_file = cls.__decode_if_needed(location)
        AWSClients.s3().download_file(Bucket=s3_file.bucket, Key=s3_file.file_path, Filename=local_path)

    @classmethod
    def upload_file(cls, local_path: str, s3_location: S3File | str):
        s3_file = cls.__decode_if_needed(s3_location)
        AWSClients.s3().upload_file(Filename=local_path, Bucket=s3_file.bucket, Key=s3_file.file_path)

# vim: set ft=python nospell syntax=python nowrap tabstop=4 expandtab shiftwidth=4 softtabstop=4:
