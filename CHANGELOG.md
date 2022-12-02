# Changelog

## [Unreleased] [2.0.0] - ?
**WeasyPrint: v54**

Summary: WeasyPrint v53+, ARM multi-arch and much smaller image.

### Breaking Changes
- Updated to WeasyPrint v53 (includes visual changes)
    [#115](https://github.com/mormahr/pdf-service/pull/115)
- Updated to WeasyPrint v54
    [#209](https://github.com/mormahr/pdf-service/pull/209)
- Switched base image from debian buster to alpine v3.14 (includes visual changes)
    [#119](https://github.com/mormahr/pdf-service/pull/119)
- Enable [HTML presentational hints][whatwg-presentational-hints] [option in WeasyPrint][weasyprint-presentational-hints]
    [#156](https://github.com/mormahr/pdf-service/pull/156)

### Improvements
- Reduced Docker image size from 363.98 MB (v1.1) to 59.48 MB (v2)
    [#136](https://github.com/mormahr/pdf-service/pull/136)
    [#137](https://github.com/mormahr/pdf-service/pull/137)
    [#141](https://github.com/mormahr/pdf-service/pull/141)
    [#157](https://github.com/mormahr/pdf-service/pull/157)
    [#158](https://github.com/mormahr/pdf-service/pull/158)
    [#161](https://github.com/mormahr/pdf-service/pull/161)
    [#163](https://github.com/mormahr/pdf-service/pull/163)
    [#164](https://github.com/mormahr/pdf-service/pull/164)
    [#165](https://github.com/mormahr/pdf-service/pull/165)
- Added support for ARM64 (Apple Silicon, AWS Graviton, etc.) architecture
    [#162](https://github.com/mormahr/pdf-service/pull/162)
    [#170](https://github.com/mormahr/pdf-service/pull/170)
- Added support for `data:` URIs
    [#224](https://github.com/mormahr/pdf-service/pull/224)
- Using [tini](https://github.com/krallin/tini) as the entrypoint
    [#134](https://github.com/mormahr/pdf-service/pull/134)
- Disabled Sentry performance sampling of `/health` endpoint
    [#174](https://github.com/mormahr/pdf-service/pull/174)

## [1.1.0] - 2021-09-01
**WeasyPrint: v52.5**

### Improvements
- Docker `HEALTHCHECK`
  [#129](https://github.com/mormahr/pdf-service/pull/129)
- Updated Python to v3.9.7
  [#107](https://github.com/mormahr/pdf-service/pull/107)

### Bug Fixes
- Fix container shutdown by using `exec` to forward signals
  [#125](https://github.com/mormahr/pdf-service/pull/125)
  ([jpxd](https://github.com/jpxd))
- Fix worker timing out regularly
  [#124](https://github.com/mormahr/pdf-service/issues/124)
  [#126](https://github.com/mormahr/pdf-service/pull/126)
  ([jpxd](https://github.com/jpxd))

## [1.0.0] - 2021-08-19
**WeasyPrint: v52.5**

Initial public release 🎉

[whatwg-presentational-hints]: https://html.spec.whatwg.org/multipage/rendering.html#the-css-user-agent-style-sheet-and-presentational-hints
[weasyprint-presentational-hints]: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html#weasyprint.HTML.render
