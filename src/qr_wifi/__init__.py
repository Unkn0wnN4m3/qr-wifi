"""
qr-wifi: Generate QR codes for WiFi credentials.

This package provides tools to create QR codes for WiFi network credentials
that can be scanned by mobile devices to automatically connect to networks.
"""

__version__ = "0.1.0"

# Public API
from qr_wifi.cli import main
from qr_wifi.exceptions import (
    InvalidPasswordError,
    InvalidSecurityTypeError,
    InvalidSSIDError,
    QRGenerationError,
    WiFiConfigError,
)
from qr_wifi.qr_generator import QRGenerator
from qr_wifi.wifi import WiFiConfig

__all__ = [
    # Main entry point
    "main",
    # Core classes
    "WiFiConfig",
    "QRGenerator",
    # Exceptions
    "WiFiConfigError",
    "InvalidSSIDError",
    "InvalidPasswordError",
    "InvalidSecurityTypeError",
    "QRGenerationError",
]


if __name__ == "__main__":
    main()
