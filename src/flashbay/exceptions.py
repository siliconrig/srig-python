"""flashbay exception hierarchy."""


class FlashbayError(Exception):
    """Base exception for all flashbay errors."""


class AuthError(FlashbayError):
    """Authentication or authorization failure."""


class SessionError(FlashbayError):
    """Session lifecycle error (create, end, not found)."""


class FlashError(FlashbayError):
    """Firmware flashing failed."""


class SerialTimeout(FlashbayError):
    """Serial read/expect timed out."""
