import json
from typing import Generator
from unittest.mock import MagicMock, patch

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_s3, mock_sns, mock_sqs  # type: ignore[import]
from mypy_boto3_s3.service_resource import Bucket
from mypy_boto3_sns.service_resource import Topic
from mypy_boto3_sqs.service_resource import Queue

import boto3_oversize


@pytest.fixture
def bucket() -> Generator[Bucket, None, None]:
    mock_s3().start()
    s3_client = boto3.resource('s3')
    bucket: Bucket = s3_client.create_bucket(Bucket='oversize-payload-bucket')
    yield bucket
    mock_s3().stop()


@pytest.fixture
def topic(bucket: Bucket) -> Generator[Topic, None, None]:
    mock_sns().start()
    sns_client = boto3_oversize.resource('sns')
    topic: Topic = sns_client.create_topic(Name='large-payload-test')
    yield topic
    mock_sns().stop()


@pytest.fixture
def queue(topic: Topic) -> Generator[Queue, None, None]:
    mock_sqs().start()
    sqs_client = boto3_oversize.resource('sqs')
    queue: Queue = sqs_client.create_queue(QueueName='large-payload-test')
    topic.subscribe(Protocol='sqs', Endpoint=queue.attributes['QueueArn'])
    yield queue
    mock_sqs().stop()


@patch('boto3_oversize.oversize.getenv', return_value='oversize-payload-bucket')
def test_resource_oversized_publish(getenv: MagicMock,
                                    bucket: Bucket, topic: Topic, queue: Queue) -> None:
    payload = '0' * boto3_oversize.oversize.MAX_PAYLOAD_SIZE
    topic.publish(Message=payload)

    messages = queue.receive_messages()
    assert json.loads(messages[0].body).get('Message') == payload
    assert len(list(bucket.objects.all())) == 1


@patch('boto3_oversize.oversize.getenv', return_value='oversize-payload-bucket')
def test_resource_oversized_publish_raw(getenv: MagicMock,
                                        bucket: Bucket, topic: Topic, queue: Queue) -> None:
    next(iter(topic.subscriptions.all())).set_attributes(AttributeName='RawMessageDelivery',
                                                         AttributeValue='true')

    payload = '0' * boto3_oversize.oversize.MAX_PAYLOAD_SIZE
    topic.publish(Message=payload)

    messages = queue.receive_messages()
    assert messages[0].body == payload
    assert len(list(bucket.objects.all())) == 1


@patch('boto3_oversize.oversize.getenv', return_value='oversize-payload-bucket')
def test_resource_oversized_publish_multi(getenv: MagicMock,
                                          bucket: Bucket, topic: Topic, queue: Queue) -> None:
    payloads = [
        '0' * boto3_oversize.oversize.MAX_PAYLOAD_SIZE,
        '1' * boto3_oversize.oversize.MAX_PAYLOAD_SIZE,
        '2' * boto3_oversize.oversize.MAX_PAYLOAD_SIZE,
    ]
    for payload in payloads:
        topic.publish(Message=payload)

    messages = queue.receive_messages(MaxNumberOfMessages=10)
    assert json.loads(messages[0].body).get('Message') == payloads[0]
    assert json.loads(messages[1].body).get('Message') == payloads[1]
    assert json.loads(messages[2].body).get('Message') == payloads[2]
    assert len(list(bucket.objects.all())) == 3


@patch('boto3_oversize.oversize.getenv', return_value=None)
def test_resource_oversized_publish_notset(getenv: MagicMock,
                                           bucket: Bucket, topic: Topic, queue: Queue) -> None:
    with pytest.raises(ClientError):
        payload = '0' * boto3_oversize.oversize.MAX_PAYLOAD_SIZE
        topic.publish(Message=payload)


@patch('boto3_oversize.oversize.getenv', return_value='oversize-payload-bucket')
def test_resource_undersized_publish(getenv: MagicMock,
                                     bucket: Bucket, topic: Topic, queue: Queue) -> None:
    payload = '0' * int(boto3_oversize.oversize.MAX_PAYLOAD_SIZE / 2)
    topic.publish(Message=payload)

    messages = queue.receive_messages()
    assert json.loads(messages[0].body).get('Message') == payload
    assert len(list(bucket.objects.all())) == 0


@patch('boto3_oversize.oversize.getenv', return_value='oversize-payload-bucket')
def test_resource_undersized_publish_raw(getenv: MagicMock,
                                         bucket: Bucket, topic: Topic, queue: Queue) -> None:
    next(iter(topic.subscriptions.all())).set_attributes(AttributeName='RawMessageDelivery',
                                                         AttributeValue='true')

    payload = '0' * int(boto3_oversize.oversize.MAX_PAYLOAD_SIZE / 2)
    topic.publish(Message=payload)

    messages = queue.receive_messages()
    assert messages[0].body == payload
    assert len(list(bucket.objects.all())) == 0


@patch('boto3_oversize.oversize.getenv', return_value='oversize-payload-bucket')
def test_resource_undersized_publish_raw_json(getenv: MagicMock,
                                              bucket: Bucket, topic: Topic, queue: Queue) -> None:
    next(iter(topic.subscriptions.all())).set_attributes(AttributeName='RawMessageDelivery',
                                                         AttributeValue='true')

    payload = '{"foo": "bar"}'
    topic.publish(Message=payload)

    messages = queue.receive_messages()
    assert messages[0].body == payload
    assert len(list(bucket.objects.all())) == 0


@patch('boto3_oversize.oversize.getenv', return_value='oversize-payload-bucket')
def test_client_oversized_publish(getenv: MagicMock,
                                  bucket: Bucket, topic: Topic, queue: Queue) -> None:
    payload = '0' * boto3_oversize.oversize.MAX_PAYLOAD_SIZE
    sns_client = boto3_oversize.client('sns')
    sns_client.publish(TopicArn=topic.arn, Message=payload)

    sqs_client = boto3_oversize.client('sqs')
    response = sqs_client.receive_message(QueueUrl=queue.url)
    assert json.loads(response['Messages'][0]['Body']).get('Message') == payload
    assert len(list(bucket.objects.all())) == 1
