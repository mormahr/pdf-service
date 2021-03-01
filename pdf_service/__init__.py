import logging
from sentry_sdk import init, set_tag
from flask import Flask, request, make_response
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import os

from .generate import generate
from .URLFetchHandler import URLFetchHandler


pdf_service = Flask(__name__)
sentry_logging = LoggingIntegration(
    level=logging.DEBUG,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
    release=os.environ.get("SENTRY_RELEASE"),
    server_name=os.environ.get("HOST"),
    integrations=[FlaskIntegration(), sentry_logging],
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
)

for k, v in os.environ.items():
    if k.startswith("SENTRY_TAG"):
        processed_key = k.replace("SENTRY_TAG_", "").lower()
        set_tag(processed_key, v)


@pdf_service.route('/generate', methods=['POST'])
def generate_pdf():
    return generate()


@pdf_service.route('/health', methods=['GET'])
def health():
    response = make_response("Healthy")
    return response


if __name__ == '__main__':
    pdf_service.run()
