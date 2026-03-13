"""Tests for flashbay.Client."""

import os
from unittest.mock import MagicMock, patch

import pytest

from flashbay.client import Client, _check
from flashbay.exceptions import AuthError, SessionError


class TestClientInit:
    def test_requires_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("FLASHBAY_API_KEY", None)
            with pytest.raises(AuthError, match="No API key"):
                Client()

    def test_reads_env_var(self):
        with patch.dict(os.environ, {"FLASHBAY_API_KEY": "sk_test_123"}):
            c = Client()
            assert c.api_key == "sk_test_123"
            c.close()

    def test_explicit_key_overrides_env(self):
        with patch.dict(os.environ, {"FLASHBAY_API_KEY": "sk_env"}):
            c = Client(api_key="sk_explicit")
            assert c.api_key == "sk_explicit"
            c.close()

    def test_custom_base_url(self):
        c = Client(api_key="sk_test", base_url="http://localhost:8080")
        assert c.base_url == "http://localhost:8080"
        c.close()

    def test_strips_trailing_slash(self):
        c = Client(api_key="sk_test", base_url="http://localhost:8080/")
        assert c.base_url == "http://localhost:8080"
        c.close()


class TestCheck:
    def test_success_passes(self):
        resp = MagicMock()
        resp.is_success = True
        _check(resp)  # should not raise

    def test_401_raises_auth_error(self):
        resp = MagicMock()
        resp.is_success = False
        resp.status_code = 401
        resp.json.return_value = {"error": "invalid key"}
        with pytest.raises(AuthError, match="invalid key"):
            _check(resp)

    def test_500_raises_session_error(self):
        resp = MagicMock()
        resp.is_success = False
        resp.status_code = 500
        resp.json.return_value = {"error": "internal"}
        with pytest.raises(SessionError, match="internal"):
            _check(resp)
