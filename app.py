from flask import Flask, request, make_response
from weasyprint import HTML

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def make_pdf():
    data = request.get_data(as_text=True)
    html = HTML(string=data)
    doc = html.render()
    pdf = doc.write_pdf()

    response = make_response(pdf)

    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment; filename="generated.pdf"')

    return response


if __name__ == '__main__':
    app.run()
