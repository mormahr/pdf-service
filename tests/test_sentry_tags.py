import os

import sentry_sdk
from pytest_mock import MockerFixture

from pdf_service import apply_sentry_tags


def test_adds_sentry_tag(mocker: MockerFixture):
    mocker.patch("os.environ.items")
    mocker.patch("sentry_sdk.set_tag")
    os.environ.items.return_value = [('SENTRY_TAG_TEST', 'abc'), ('OTHER_VAR', 'unrelated')]

    apply_sentry_tags()

    sentry_sdk.set_tag.assert_called_once_with("test", "abc")


def test_adds_sentry_tag_with_multiple_parts(mocker: MockerFixture):
    mocker.patch("os.environ.items")
    mocker.patch("sentry_sdk.set_tag")
    os.environ.items.return_value = [('SENTRY_TAG_LONGER_VALUE', 'the-value')]

    apply_sentry_tags()

    sentry_sdk.set_tag.assert_called_once_with("longer_value", "the-value")


def test_adds_sentry_tags(mocker: MockerFixture):
    mocker.patch("os.environ.items")
    mocker.patch("sentry_sdk.set_tag")
    os.environ.items.return_value = [('SENTRY_TAG_VALUE_A', 'a'), ('SENTRY_TAG_VALUE_B', 'B')]

    apply_sentry_tags()

    sentry_sdk.set_tag.assert_any_call("value_a", "a")
    sentry_sdk.set_tag.assert_any_call("value_b", "B")
