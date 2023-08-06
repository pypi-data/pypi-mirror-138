import re

import pytest

from boto3_oversize.oversize import generate_payload_key, is_offloaded_payload, is_oversize_payload


@pytest.mark.parametrize(['payload_len', 'oversized'], [
    (0, False),
    (1, False),
    (245759, False),
    (245760, True),
    (262144, True),
    (524288, True),
])
def test_is_oversize_payload(payload_len: int, oversized: bool) -> None:
    payload = '0' * payload_len
    assert is_oversize_payload(payload) == oversized


@pytest.mark.parametrize(['payload', 'offloaded'], [
    ('0000000000000000', False),
    ('https://example.com/', False),
    ('arn:aws:s3:::payload-bucket/example.txt', False),
    ('arn:aws:s3:::example.com/f4310c00-2479-4c76-91d4-b61a5083c002', True),
    ('arn:aws:s3:::payload-bucket/f4310c00-2479-4c76-91d4-b61a5083c002', True),
])
def test_is_offloaded_payload(payload: str, offloaded: bool) -> None:
    assert is_offloaded_payload(payload) == offloaded


def test_generate_payload_key() -> None:
    key = generate_payload_key()
    assert re.match(r'^[\d\w-]+$', key) is not None
