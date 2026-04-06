"""Tests for siliconrig.Serial."""

import json
import threading
import time
from unittest.mock import patch

import pytest

from siliconrig.exceptions import SerialTimeout
from siliconrig.serial import Serial


@pytest.fixture
def serial_conn(fake_ws):
    with patch("siliconrig.serial.ws_sync.connect", return_value=fake_ws):
        s = Serial("ws://localhost/serial", "sk_test")
        yield s, fake_ws
        s.close()


class TestSend:
    def test_sends_json_frame(self, serial_conn):
        serial, ws = serial_conn
        serial.send("hello\n")
        sent = json.loads(ws._sent[-1])
        assert sent == {"type": "serial_data", "data": "hello\n"}


class TestRead:
    def test_reads_buffered_data(self, serial_conn):
        serial, ws = serial_conn
        ws.inject("serial_data", "boot ok\n")
        time.sleep(0.15)
        result = serial.read(timeout=1)
        assert "boot ok" in result

    def test_timeout_raises(self, serial_conn):
        serial, _ = serial_conn
        with pytest.raises(SerialTimeout):
            serial.read(timeout=0.2)


class TestReadUntil:
    def test_finds_pattern(self, serial_conn):
        serial, ws = serial_conn
        ws.inject("serial_data", "loading... ")
        ws.inject("serial_data", "Ready\n")
        time.sleep(0.15)
        result = serial.read_until("Ready", timeout=2)
        assert "Ready" in result

    def test_timeout_shows_received(self, serial_conn):
        serial, ws = serial_conn
        ws.inject("serial_data", "partial")
        time.sleep(0.15)
        with pytest.raises(SerialTimeout, match="partial"):
            serial.read_until("NEVER", timeout=0.3)


class TestExpect:
    def test_expect_is_read_until(self, serial_conn):
        serial, ws = serial_conn
        ws.inject("serial_data", "System ready\n")
        time.sleep(0.15)
        result = serial.expect("ready", timeout=2)
        assert "ready" in result


class TestFlush:
    def test_clears_buffer(self, serial_conn):
        serial, ws = serial_conn
        ws.inject("serial_data", "noise")
        time.sleep(0.15)
        serial.flush()
        with pytest.raises(SerialTimeout):
            serial.read(timeout=0.2)
