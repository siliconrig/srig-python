"""pytest plugin — auto-registered via the ``pytest11`` entry point.

Provides the ``flashbay_board`` fixture and CLI options.
"""

import pytest

from flashbay.board import Board


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("flashbay", "flashbay hardware-in-the-loop testing")
    group.addoption(
        "--flashbay-board",
        dest="flashbay_board",
        default=None,
        help="Board type to use for flashbay sessions (e.g. esp32s3).",
    )
    group.addoption(
        "--flashbay-firmware",
        dest="flashbay_firmware",
        default=None,
        help="Path to firmware binary to flash before tests.",
    )
    group.addoption(
        "--flashbay-api-key",
        dest="flashbay_api_key",
        default=None,
        help="API key (overrides FLASHBAY_API_KEY env var).",
    )
    group.addoption(
        "--flashbay-base-url",
        dest="flashbay_base_url",
        default=None,
        help="Coordinator base URL (overrides FLASHBAY_BASE_URL env var).",
    )


@pytest.fixture(scope="session")
def flashbay_board(request: pytest.FixtureRequest):
    """Session-scoped fixture that provides a flashed, ready-to-use board.

    Configure via CLI options or environment variables::

        pytest --flashbay-board esp32s3 --flashbay-firmware build/app.bin

    Or use the ``Board`` class directly in your own fixtures for more control.
    """
    board_type = request.config.getoption("flashbay_board")
    if board_type is None:
        pytest.skip("No --flashbay-board specified; skipping HIL tests")

    firmware = request.config.getoption("flashbay_firmware")
    api_key = request.config.getoption("flashbay_api_key")
    base_url = request.config.getoption("flashbay_base_url")

    with Board(
        board_type,
        firmware=firmware,
        api_key=api_key,
        base_url=base_url,
    ) as board:
        yield board
