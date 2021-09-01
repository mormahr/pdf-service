# Changelog

## [Unreleased] [2.0.0] - ?
**WeasyPrint: v53.2**

Summary: WeasyPrint v53, alpine and much smaller image.

### Breaking Changes
- Updated to WeasyPrint v53 (includes visual changes)
    [#115](https://github.com/mormahr/pdf-service/pull/115)
- Switched base image from debian buster to alpine v3.14 (includes visual changes)
    [#119](https://github.com/mormahr/pdf-service/pull/119)

### Improvements
- Reduced Docker image size from 363.98 MB (v1.1) to 176.67 MB (v2)
    [#136](https://github.com/mormahr/pdf-service/pull/136)
    [#137](https://github.com/mormahr/pdf-service/pull/137)
    [#141](https://github.com/mormahr/pdf-service/pull/141)
- Using [tini](https://github.com/krallin/tini) as the entrypoint
    [#134](https://github.com/mormahr/pdf-service/pull/134)

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
