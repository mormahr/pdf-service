from io import BytesIO
from typing import Optional

from flask import make_response, request, Response
from sentry_sdk import start_span, set_context
from weasyprint import HTML
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

from .URLFetchHandler import URLFetchHandler


def generate() -> Response:
    with start_span(op='decode'):
        if request.files:
            # Multipart
            html_file: Optional[FileStorage] = request.files.get("index.html")
            html_size = html_file.content_length
            if html_file is None:
                raise BadRequest("No index.html present")

        else:
            # Basic
            html_file: BytesIO = BytesIO(request.get_data())
            html_size = html_file.getbuffer().nbytes

    with URLFetchHandler(request.files) as url_fetcher:
        with start_span(op='parse'):
            html = HTML(file_obj=html_file, url_fetcher=url_fetcher)

        with start_span(op='render'):
            doc = html.render()

    with start_span(op='write-pdf'):
        pdf = doc.write_pdf()

    set_context("pdf-details", {
        "html_size": html_size,
        "pdf_size": len(pdf),
    })

    response = make_response(pdf)

    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment; filename="generated.pdf"')

    return response
