"""Custom exceptions for qr-wifi package."""


class WiFiConfigError(Exception):
    """Base exception for WiFi configuration errors."""

    pass


class InvalidSSIDError(WiFiConfigError):
    """Raised when SSID is invalid."""

    pass


class InvalidPasswordError(WiFiConfigError):
    """Raised when password is invalid for the given security type."""

    pass


class InvalidSecurityTypeError(WiFiConfigError):
    """Raised when security type is not supported."""

    pass


class QRGenerationError(Exception):
    """Raised when QR code generation fails."""

    pass
