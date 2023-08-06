import analytics
import asyncio

from typing import Callable
from functools import wraps

from relevanceai.config import CONFIG
from relevanceai.json_encoder import json_encoder


def enable_tracking():
    if CONFIG.is_field("mixpanel.enable_tracking"):
        return CONFIG.get_field("mixpanel.enable_tracking", CONFIG.config)


def track(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if enable_tracking():

                async def send_analytics():
                    user_id = args[0].firebase_uid
                    event = f"pysdk-{func.__name__}"
                    kwargs.update(dict(zip(func.__code__.co_varnames, args)))
                    properties = {
                        "args": args,
                        "kwargs": kwargs,
                    }
                    if user_id is not None:
                        analytics.track(
                            user_id=user_id,
                            event=json_encoder(event, force_string=True),
                            properties=json_encoder(properties, force_string=True),
                        )

                asyncio.ensure_future(send_analytics())
        except Exception as e:
            pass

        return func(*args, **kwargs)

    return wrapper


def identify(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            if enable_tracking():
                user_id = args[0].firebase_uid
                region = args[0].region
                traits = {
                    "region": region,
                }
                if user_id is not None:
                    analytics.identify(user_id, traits)
        except Exception as e:
            pass

        return func(*args, **kwargs)

    return wrapper
