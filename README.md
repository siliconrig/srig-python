# flashbay

Python SDK for [flashbay](https://flashbay.dev) — remote access to MCU development boards.

Use it in scripts, automation, or as a pytest plugin for hardware-in-the-loop testing.

## Install

```bash
pip install flashbay
```

## Quick start

```python
from flashbay import Client

client = Client()

with client.session(board="esp32s3") as session:
    session.flash("firmware.bin")
    session.serial.expect("Ready", timeout=10)
    session.serial.send("status\n")
    print(session.serial.read_until("OK", timeout=5))
```

Or use the `Board` shorthand:

```python
from flashbay import Board

with Board("esp32-s3", firmware="build/app.bin") as board:
    board.expect("System ready", timeout=5)
    board.send("gpio set 4 1\n")
    board.expect("GPIO4=HIGH", timeout=2)
```

## pytest plugin

The package includes a pytest plugin that registers automatically. Use it with custom fixtures:

```python
import pytest
from flashbay import Board

@pytest.fixture
def board():
    with Board("esp32-s3", firmware="build/app.bin") as b:
        yield b

def test_boot_ok(board):
    assert board.expect("System ready", timeout=5)
```

Or use the built-in `flashbay_board` fixture via CLI options:

```bash
pytest --flashbay-board esp32s3 --flashbay-firmware build/app.bin tests/hil/
```

## Authentication

Set your API key via environment variable:

```bash
export FLASHBAY_API_KEY=key_...
```

Or pass it directly:

```python
client = Client(api_key="key_...")
```

## Documentation

- [Python SDK guide](https://flashbay.dev/docs/guides/python-sdk)
- [CI/CD integration](https://flashbay.dev/docs/guides/cicd)
