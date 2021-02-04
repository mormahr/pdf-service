from sentry_sdk import init, start_span, set_context
from flask import Flask, request, make_response
from weasyprint import HTML
from sentry_sdk.integrations.flask import FlaskIntegration
import os

app = Flask(__name__)
init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
    release=os.environ.get("GITHUB_SHA"),
    server_name=os.environ.get("HOST"),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)


@app.route('/generate', methods=['POST'])
def generate_pdf():
    with start_span(op='decode'):
        data = request.get_data(as_text=True)

    with start_span(op='parse'):
        html = HTML(string=data)

    with start_span(op='render'):
        doc = html.render()

    with start_span(op='write-pdf'):
        pdf = doc.write_pdf()

    set_context("pdf-details", {
        "html_size": len(data),
        "pdf_size": len(pdf),
    })

    response = make_response(pdf)

    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment; filename="generated.pdf"')

    return response


@app.route('/health', methods=['GET'])
def health():
    response = make_response("Healthy")
    return response


if __name__ == '__main__':
    app.run()
