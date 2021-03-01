from io import BytesIO

from flask import make_response, Response, request
from sentry_sdk import start_span, set_context
from weasyprint import HTML

from .URLFetchHandler import URLFetchHandler


def generate_basic() -> Response:
    with start_span(op='decode'):
        html_file = BytesIO(request.get_data())

    with URLFetchHandler(request.files) as url_fetcher:
        with start_span(op='parse'):
            html = HTML(file_obj=html_file, url_fetcher=url_fetcher)

        with start_span(op='render'):
            doc = html.render()

    with start_span(op='write-pdf'):
        pdf = doc.write_pdf()

    set_context("pdf-details", {
        "html_size": html_file.getbuffer().nbytes,
        "pdf_size": len(pdf),
    })

    response = make_response(pdf)

    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment; filename="generated.pdf"')

    return response
