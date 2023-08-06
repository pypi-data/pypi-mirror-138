from typing import Any

import boto3

from .oversize import intercept_publish_params, intercept_receive_message


def session(*args: Any, **kwargs: Any) -> boto3.Session:
    session = boto3.Session(*args, **kwargs)
    session.events.register('provide-client-params.sns.Publish',  # type: ignore[attr-defined]
                            intercept_publish_params)
    session.events.register('creating-client-class.sqs',  # type: ignore[attr-defined]
                            intercept_receive_message)
    return session


def client(*args: Any, **kwargs: Any) -> Any:
    return session().client(*args, **kwargs)


def resource(*args: Any, **kwargs: Any) -> Any:
    return session().resource(*args, **kwargs)
