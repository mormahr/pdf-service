from sentry_sdk import init, set_tag
from flask import Flask, request, make_response
from sentry_sdk.integrations.flask import FlaskIntegration
import os

from .generate_basic import generate_basic
from .URLFetchHandler import URLFetchHandler
from .errors import ForbiddenURLFetchError


pdf_service = Flask(__name__)
init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
    release=os.environ.get("SENTRY_RELEASE"),
    server_name=os.environ.get("HOST"),
    integrations=[FlaskIntegration()],
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
)

for k, v in os.environ.items():
    if k.startswith("SENTRY_TAG"):
        processed_key = k.replace("SENTRY_TAG_", "").lower()
        set_tag(processed_key, v)


@pdf_service.route('/generate', methods=['POST'])
def generate_pdf():
    return generate_basic(request)


@pdf_service.route('/health', methods=['GET'])
def health():
    response = make_response("Healthy")
    return response


if __name__ == '__main__':
    pdf_service.run()
