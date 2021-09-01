import fire
from pdf2image import convert_from_bytes
from weasyprint import HTML
from pathlib import Path


def create(name):
    """
    Creates a new reference image from an html file.
    Place the html file into the test-data folder.

    :param name: name of the test case without the file extension
    :return:
    """

    base = Path(__file__).parent.joinpath("../test-data")
    pdf_file = base.joinpath(name + ".pdf").absolute()

    def url_fetcher(url: str):
        return {
            'file_obj': base.joinpath(name).joinpath(url.removeprefix("file:///")).open('rb')
        }

    html = HTML(filename=base.joinpath(name + ".html").absolute(), url_fetcher=url_fetcher)
    doc = html.render()

    pdf = doc.write_pdf()
    with open(pdf_file, mode="wb") as f:
        f.write(pdf)

    convert_from_bytes(pdf,
                       output_file=name + "_",
                       output_folder=base.absolute(),
                       fmt="png",
                       paths_only=True)


def update():
    """
    Updates or creates all reference images from the html files.

    :return:
    """
    base = Path(__file__).parent.parent.joinpath("./test-data")
    for input_file in base.glob("*.html"):
        case = input_file.stem
        print("Processing test case:", case)

        for result in base.glob(case + "*.png"):
            print("Removing old result:", result.stem)
            result.unlink()

        print("Updating test case:", case)
        create(case)


if __name__ == "__main__":
    fire.Fire({
        "create": create,
        "update": update,
    })
