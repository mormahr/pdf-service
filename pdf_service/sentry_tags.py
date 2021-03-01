import os

import sentry_sdk


def apply_sentry_tags():
    for k, v in os.environ.items():
        if k.startswith("SENTRY_TAG"):
            processed_key = k.replace("SENTRY_TAG_", "").lower()
            sentry_sdk.set_tag(processed_key, v)
