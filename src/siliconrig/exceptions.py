"""siliconrig exception hierarchy."""


class SiliconrigError(Exception):
    """Base exception for all siliconrig errors."""


class AuthError(SiliconrigError):
    """Authentication or authorization failure."""


class SessionError(SiliconrigError):
    """Session lifecycle error (create, end, not found)."""


class FlashError(SiliconrigError):
    """Firmware flashing failed."""


class SerialTimeout(SiliconrigError):
    """Serial read/expect timed out."""
