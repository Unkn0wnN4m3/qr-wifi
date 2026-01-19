"""WiFi configuration with validation."""

import re

from qr_wifi.exceptions import (
    InvalidPasswordError,
    InvalidSecurityTypeError,
    InvalidSSIDError,
)

# Supported security types
SECURITY_TYPES = ["WPA", "WPA2", "WEP", "nopass"]

# Characters that need to be escaped in WiFi QR format
SPECIAL_CHARS = {";", ":", ",", "\\", '"'}


class WiFiConfig:
    """
    WiFi configuration with validation.

    Attributes:
        ssid: Network SSID (1-32 characters)
        security: Security type (WPA, WPA2, WEP, nopass)
        password: Network password (optional for nopass)
        hidden: Whether the network is hidden (default: False)
    """

    def __init__(
        self, ssid: str, security: str, password: str = "", hidden: bool = False
    ) -> None:
        """
        Initialize WiFi configuration with validation.

        Args:
            ssid: Network SSID
            security: Security type
            password: Network password
            hidden: Whether network is hidden

        Raises:
            InvalidSSIDError: If SSID is invalid
            InvalidSecurityTypeError: If security type is not supported
            InvalidPasswordError: If password is invalid for security type
        """
        self.ssid = ssid
        # Normalize security type, but keep 'nopass' lowercase
        self.security = security if security.lower() == "nopass" else security.upper()
        self.password = password
        self.hidden = hidden

        self._validate()

    def _validate(self) -> None:
        """Validate WiFi configuration."""
        self._validate_ssid()
        self._validate_security()
        self._validate_password()

    def _validate_ssid(self) -> None:
        """Validate SSID."""
        if not self.ssid:
            raise InvalidSSIDError("SSID cannot be empty")

        if len(self.ssid) > 32:
            raise InvalidSSIDError(
                f"SSID too long: {len(self.ssid)} characters (max 32)"
            )

    def _validate_security(self) -> None:
        """Validate security type."""
        if self.security not in SECURITY_TYPES:
            raise InvalidSecurityTypeError(
                f"Security type '{self.security}' not supported. "
                f"Valid options: {', '.join(SECURITY_TYPES)}"
            )

    def _validate_password(self) -> None:
        """Validate password based on security type."""
        if self.security == "nopass":
            # No password required for open networks
            return

        if not self.password:
            raise InvalidPasswordError(
                f"Password required for {self.security} security"
            )

        if self.security in ["WPA", "WPA2"]:
            if len(self.password) < 8:
                raise InvalidPasswordError(
                    f"WPA/WPA2 password must be at least 8 characters "
                    f"(got {len(self.password)})"
                )
            if len(self.password) > 63:
                raise InvalidPasswordError(
                    f"WPA/WPA2 password must be at most 63 characters "
                    f"(got {len(self.password)})"
                )

        elif self.security == "WEP":
            # WEP keys are hex strings with specific lengths
            if not re.match(r"^[0-9A-Fa-f]+$", self.password):
                raise InvalidPasswordError("WEP password must be hexadecimal")

            if len(self.password) not in [10, 26, 58]:
                raise InvalidPasswordError(
                    f"WEP password must be 10, 26, or 58 hex characters "
                    f"(got {len(self.password)})"
                )

    @staticmethod
    def _escape_special_chars(text: str) -> str:
        """
        Escape special characters for WiFi QR format.

        Args:
            text: Text to escape

        Returns:
            Escaped text
        """
        # Escape backslash first to avoid double escaping
        result = text.replace("\\", "\\\\")
        # Then escape other special characters
        for char in [";", ":", ",", '"']:
            result = result.replace(char, f"\\{char}")
        return result

    def to_qr_string(self) -> str:
        """
        Generate WiFi QR code string.

        Returns:
            WiFi QR format string: WIFI:S:<ssid>;T:<security>;P:<password>;;

        Example:
            >>> config = WiFiConfig("MyNetwork", "WPA2", "password123")
            >>> config.to_qr_string()
            'WIFI:S:MyNetwork;T:WPA2;P:password123;;'
        """
        ssid_escaped = self._escape_special_chars(self.ssid)
        password_escaped = self._escape_special_chars(self.password)

        # Build WiFi string according to format
        parts = [f"WIFI:S:{ssid_escaped}"]

        # Security type
        parts.append(f"T:{self.security}")

        # Password (only if not open network)
        if self.security != "nopass":
            parts.append(f"P:{password_escaped}")

        # Hidden network
        if self.hidden:
            parts.append("H:true")

        return ";".join(parts) + ";;"
