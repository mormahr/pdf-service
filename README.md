# pdf-service
**WeasyPrint in Docker**

[![codecov.io](https://codecov.io/github/mormahr/pdf-service/coverage.svg?branch=main)](https://codecov.io/github/mormahr/pdf-service?branch=main)

A dockerized HTTP service, that generates PDF files from HTML using [Weasyprint][weasyprint].
The primary use-case is generation of documents from developer controlled templates, such as
invoices. It is not meant as a general webpage to PDF converter. The service expects input HTML and
other resources to be safe and doesn't do any hardening or sandboxing that would be required for
arbitrary inputs. Please consult the [security][#security] section of this document.

## API

### Basic "simple" API without asset support

Make a `POST` request to `/generate` with the HTML file you want to render as the body.
The response will be the PDF file.

```sh
curl \
  -X POST \
  -H "Content-Type: text/html" \
  --data '<p>Hello World!</p>' \
  https://pdf.example.com/generate \
  > hello_world.pdf
```

### Multipart API

Make a `POST` request to `/generate` with a `Content-Type` of `multipart/form-data`. Provide your
HTML input as `index.html` and add any other required assets. The assets can be referenced _in the 
HTML_ either as an absolute URL like `/image.png` or a relative one `image.png`. Relative URLs are
resolved against `/`. **Omit the leading slash** for the `multipart/form-data` `name` attribute.

```sh
curl \
  -F index.html=@index.html \
  -F image.png=@image.png \
  -F sub-path/image.png=@sub-path/image.png \
  https://pdf.example.com/generate \
  > hello_world.pdf
```

```html
<!-- index.html -->
<p>With an image:</p>
<img src="/image.png" />
<img src="/sub-path/image.png" />
```

## Deployment

The docker image is tagged as `mormahr/pdf-service`.
Images are continuously pushed to the `:latest` tag.

### Security

It's not recommended allowing untrusted HTML input.
Use trusted HTML templates and sanitize user inputs.

Fetching of external assets is prohibited as of now. You can add internal assets with the [multipart
API](#multipart-API).

If your instance is exposed publicly, I recommend using a reverse proxy to terminate TLS connections
and require authentication. You could use HTTP Basic Auth and then pass the pdf-service URL to your
client software via an environment variable. This way auth information can be embedded like this:
`https://API_USER:API_TOKEN@pdf.example.com/generate`, where `API_USER` and `API_TOKEN` are the
credentials you set up in the reverse proxy.

### Environment variables

- `WORKER_COUNT` (default: 4) Sets the worker pool size of the gunicorn server executing pdf_service.

- `HOST` if the hostname isn't set on the container, pass it as an environment variable to identify
    the service in Sentry.
  
- `SENTRY_DSN` Enable the Sentry integration and use this DSN to submit data.
- `SENTRY_TRACES_SAMPLE_RATE` (`0.0` ... `1.0`) If the Sentry integration is enabled this controls
  the tracing sample rate. It defaults to `1.0`. Set it to `0.0` to disable tracing.
- `SENTRY_ENVIRONMENT` This sets the environment sent to Sentry. Defaults to `development`.
- `SENTRY_RELEASE` This sets the release sent to Sentry. We set this to the current git SHA and you
  normally shouldn't need to overwrite it.
- `SENTRY_TAG_*` Set a tag to a specific value for all transactions.
  For example to set the tag `test` to `abc`, set the environment variable `SENTRY_TAG_TEST=abc`.

## Development

### Setup the development environment

- Setup python venv 
- `pip install -r requirements.txt` (or: `pip install -e '.[dev]'`)
- Install docker and docker-compose to run tests. 
  Tests run in docker to ensure render output doesn't differ based on platform.
  
### Running

- Run the development server with `python -m pdf_service`
- Run tests with `./test` or `./test-watch`
  - Tests are executed within docker, to ensure render results are identical to the containerized
    version. The image contains external dependencies, but code and test files will be mounted from
    the project source. If you want to rebuild the dev image add `--build` to the end of the
    command. This will instruct `docker-compose` to rebuild the image.

### Visual tests with reference images

`test-data` contains reference inputs `*.html` and corresponding outputs `*.png`.
A test suite will render the html files and will compare the output with the reference images to 
ensure no changes slipped in.

To update test-data or add new test cases run `./update-test-data`.

[weasyprint]: https://weasyprint.org
