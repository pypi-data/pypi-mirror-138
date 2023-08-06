import json
import re
from os import getenv
from typing import Any, Dict, Optional
from uuid import uuid4

import boto3
from mypy_boto3_sqs.client import SQSClient
from mypy_boto3_sqs.type_defs import ReceiveMessageResultTypeDef

"""
Maximum allowed SNS and SQS message size (256KiB).
"""
MAX_PAYLOAD_SIZE = 2 ** 18

"""
When raw message delivery is disabled and messages are delivered to SQS, SNS encodes the message
as JSON and adds metadata about the message and topic to the payload. This overhead needs to be
considered when determining whether a message can fit within the maximum allowed payload size.
"""
ENVELOPE_OVERHEAD = 1 / 16

OVERSIZE_PAYLOAD_THRESHOLD = int(MAX_PAYLOAD_SIZE * (1 - ENVELOPE_OVERHEAD))


def is_oversize_payload(payload: str) -> bool:
    return len(payload) >= OVERSIZE_PAYLOAD_THRESHOLD


def is_offloaded_payload(payload: str) -> bool:
    return re.match(r'^arn:aws:s3:::[\d\w\.-]{3,63}/[\d\w-]+$', payload) is not None


def generate_payload_key() -> str:
    return str(uuid4())


def store_payload(payload: str) -> Optional[str]:
    bucket, key = getenv('OVERSIZE_PAYLOAD_BUCKET_NAME'), generate_payload_key()
    if not bucket:
        return None
    boto3.client('s3').put_object(Bucket=bucket, Body=payload.encode('utf8'), Key=key)
    return f'arn:aws:s3:::{bucket}/{key}'


def retrieve_payload(payload: str) -> str:
    bucket, key = str(payload).split(':').pop(-1).split('/')
    return boto3.client('s3').get_object(Bucket=bucket, Key=key)['Body'].read().decode('utf8')


def intercept_publish_params(params: Dict[str, Any], **kwargs: Any) -> None:
    if is_oversize_payload(params['Message']):
        payload_arn = store_payload(params['Message'])
        if payload_arn:
            params['Message'] = payload_arn


def intercept_receive_message(class_attributes: Dict[str, Any],  # noqa: C901
                              **kwargs: Any) -> None:
    original_receive_message = class_attributes['receive_message']

    def receive_message(self: SQSClient, **kwargs: Any) -> ReceiveMessageResultTypeDef:
        response: ReceiveMessageResultTypeDef = original_receive_message(self, **kwargs)
        for message in response.get('Messages', []):
            try:
                # SQS message is JSON with SNS "Message" inside
                body = json.loads(message['Body'])
                assert body['Type'] == 'Notification'
                if is_offloaded_payload(body['Message']):
                    body['Message'] = retrieve_payload(body['Message'])
                    message['Body'] = json.dumps(body)
            except (json.decoder.JSONDecodeError, AssertionError, KeyError):
                # SQS message is raw SNS message body, or something else
                if is_offloaded_payload(message['Body']):
                    message['Body'] = retrieve_payload(message['Body'])
        return response

    class_attributes['receive_message'] = receive_message
