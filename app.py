from flask import Flask, request, make_response
from weasyprint import HTML
from elasticapm.contrib.flask import ElasticAPM
import elasticapm

app = Flask(__name__)
apm = ElasticAPM(app)


@app.route('/generate', methods=['POST'])
def make_pdf():
    with elasticapm.capture_span('decode'):
        data = request.get_data(as_text=True)

    with elasticapm.capture_span('parse'):
        html = HTML(string=data)

    with elasticapm.capture_span('render'):
        doc = html.render()

    with elasticapm.capture_span('write-pdf'):
        pdf = doc.write_pdf()

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
