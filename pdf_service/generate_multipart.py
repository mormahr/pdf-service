from typing import Optional

from flask import make_response, request, Response
from sentry_sdk import start_span, set_context
from weasyprint import HTML
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from .URLFetchHandler import URLFetchHandler


def generate_multipart() -> Response:
    with start_span(op='decode'):
        html_file: Optional[FileStorage] = request.files.get("index.html")
        if html_file is None:
            raise BadRequest("No index.html present")

    with URLFetchHandler(request.files) as url_fetcher:
        with start_span(op='parse'):
            html = HTML(file_obj=html_file, url_fetcher=url_fetcher)

        with start_span(op='render'):
            doc = html.render()

    with start_span(op='write-pdf'):
        pdf = doc.write_pdf()

    set_context("pdf-details", {
        "pdf_size": len(pdf),
    })

    response = make_response(pdf)

    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment; filename="generated.pdf"')

    return response
