# WeasyPrint in Docker

## Deployment

The docker image is tagged as `mormahr/pdf-service`.
Images are continuously pushed to the `:latest` tag.

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
- `pip install -e '.[dev]'`
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
