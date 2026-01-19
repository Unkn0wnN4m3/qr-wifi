"""Tests for WiFi configuration."""

import pytest

from qr_wifi.exceptions import (
    InvalidPasswordError,
    InvalidSecurityTypeError,
    InvalidSSIDError,
)
from qr_wifi.wifi import WiFiConfig


class TestWiFiConfigValidation:
    """Test WiFiConfig validation."""

    def test_valid_wpa2_config(self) -> None:
        """Test valid WPA2 configuration."""
        config = WiFiConfig("MyNetwork", "WPA2", "password123")
        assert config.ssid == "MyNetwork"
        assert config.security == "WPA2"
        assert config.password == "password123"
        assert config.hidden is False

    def test_valid_wpa_config(self) -> None:
        """Test valid WPA configuration."""
        config = WiFiConfig("TestNet", "WPA", "12345678")
        assert config.ssid == "TestNet"
        assert config.security == "WPA"
        assert config.password == "12345678"

    def test_valid_open_network(self) -> None:
        """Test valid open network (nopass)."""
        config = WiFiConfig("OpenNet", "nopass")
        assert config.ssid == "OpenNet"
        assert config.security == "nopass"
        assert config.password == ""

    def test_valid_wep_config(self) -> None:
        """Test valid WEP configuration."""
        config = WiFiConfig("WEPNet", "WEP", "1234567890")
        assert config.ssid == "WEPNet"
        assert config.security == "WEP"
        assert config.password == "1234567890"

    def test_hidden_network(self) -> None:
        """Test hidden network configuration."""
        config = WiFiConfig("HiddenNet", "WPA2", "password123", hidden=True)
        assert config.hidden is True

    def test_empty_ssid_raises_error(self) -> None:
        """Test that empty SSID raises error."""
        with pytest.raises(InvalidSSIDError, match="SSID cannot be empty"):
            WiFiConfig("", "WPA2", "password123")

    def test_ssid_too_long_raises_error(self) -> None:
        """Test that SSID longer than 32 characters raises error."""
        long_ssid = "a" * 33
        with pytest.raises(InvalidSSIDError, match="SSID too long"):
            WiFiConfig(long_ssid, "WPA2", "password123")

    def test_ssid_max_length_valid(self) -> None:
        """Test that SSID of exactly 32 characters is valid."""
        max_ssid = "a" * 32
        config = WiFiConfig(max_ssid, "WPA2", "password123")
        assert config.ssid == max_ssid

    def test_invalid_security_type_raises_error(self) -> None:
        """Test that invalid security type raises error."""
        with pytest.raises(InvalidSecurityTypeError, match="not supported"):
            WiFiConfig("MyNetwork", "WPA3", "password123")

    def test_security_type_case_insensitive(self) -> None:
        """Test that security type is case insensitive."""
        config = WiFiConfig("MyNetwork", "wpa2", "password123")
        assert config.security == "WPA2"

    def test_wpa_password_too_short_raises_error(self) -> None:
        """Test that WPA password shorter than 8 characters raises error."""
        with pytest.raises(InvalidPasswordError, match="at least 8 characters"):
            WiFiConfig("MyNetwork", "WPA", "1234567")

    def test_wpa2_password_too_short_raises_error(self) -> None:
        """Test that WPA2 password shorter than 8 characters raises error."""
        with pytest.raises(InvalidPasswordError, match="at least 8 characters"):
            WiFiConfig("MyNetwork", "WPA2", "short")

    def test_wpa_password_too_long_raises_error(self) -> None:
        """Test that WPA password longer than 63 characters raises error."""
        long_password = "a" * 64
        with pytest.raises(InvalidPasswordError, match="at most 63 characters"):
            WiFiConfig("MyNetwork", "WPA", long_password)

    def test_wpa_password_min_length_valid(self) -> None:
        """Test that WPA password of exactly 8 characters is valid."""
        config = WiFiConfig("MyNetwork", "WPA", "12345678")
        assert config.password == "12345678"

    def test_wpa_password_max_length_valid(self) -> None:
        """Test that WPA password of exactly 63 characters is valid."""
        max_password = "a" * 63
        config = WiFiConfig("MyNetwork", "WPA", max_password)
        assert config.password == max_password

    def test_wpa_missing_password_raises_error(self) -> None:
        """Test that missing password for WPA raises error."""
        with pytest.raises(InvalidPasswordError, match="Password required"):
            WiFiConfig("MyNetwork", "WPA", "")

    def test_wep_invalid_hex_raises_error(self) -> None:
        """Test that non-hex WEP password raises error."""
        with pytest.raises(InvalidPasswordError, match="must be hexadecimal"):
            WiFiConfig("MyNetwork", "WEP", "notahexstring")

    def test_wep_invalid_length_raises_error(self) -> None:
        """Test that WEP password with invalid length raises error."""
        with pytest.raises(InvalidPasswordError, match="must be 10, 26, or 58"):
            WiFiConfig("MyNetwork", "WEP", "123456")

    def test_wep_valid_10_char_hex(self) -> None:
        """Test valid 10 character WEP hex password."""
        config = WiFiConfig("MyNetwork", "WEP", "1234567890")
        assert config.password == "1234567890"

    def test_wep_valid_26_char_hex(self) -> None:
        """Test valid 26 character WEP hex password."""
        hex_password = "12345678901234567890123456"
        config = WiFiConfig("MyNetwork", "WEP", hex_password)
        assert config.password == hex_password

    def test_wep_valid_58_char_hex(self) -> None:
        """Test valid 58 character WEP hex password."""
        hex_password = "1234567890123456789012345678901234567890123456789012345678"
        config = WiFiConfig("MyNetwork", "WEP", hex_password)
        assert config.password == hex_password


class TestWiFiConfigQRString:
    """Test WiFi QR string generation."""

    def test_basic_qr_string(self) -> None:
        """Test basic QR string generation."""
        config = WiFiConfig("MyNetwork", "WPA2", "password123")
        qr_string = config.to_qr_string()
        assert qr_string == "WIFI:S:MyNetwork;T:WPA2;P:password123;;"

    def test_open_network_qr_string(self) -> None:
        """Test QR string for open network (no password)."""
        config = WiFiConfig("OpenNet", "nopass")
        qr_string = config.to_qr_string()
        assert qr_string == "WIFI:S:OpenNet;T:nopass;;"

    def test_hidden_network_qr_string(self) -> None:
        """Test QR string for hidden network."""
        config = WiFiConfig("HiddenNet", "WPA2", "password123", hidden=True)
        qr_string = config.to_qr_string()
        assert qr_string == "WIFI:S:HiddenNet;T:WPA2;P:password123;H:true;;"

    def test_escape_semicolon_in_ssid(self) -> None:
        """Test that semicolon in SSID is escaped."""
        config = WiFiConfig("My;Network", "WPA2", "password123")
        qr_string = config.to_qr_string()
        assert "My\\;Network" in qr_string
        assert qr_string == "WIFI:S:My\\;Network;T:WPA2;P:password123;;"

    def test_escape_colon_in_password(self) -> None:
        """Test that colon in password is escaped."""
        config = WiFiConfig("MyNetwork", "WPA2", "pass:word")
        qr_string = config.to_qr_string()
        assert "pass\\:word" in qr_string
        assert qr_string == "WIFI:S:MyNetwork;T:WPA2;P:pass\\:word;;"

    def test_escape_comma_in_ssid(self) -> None:
        """Test that comma in SSID is escaped."""
        config = WiFiConfig("My,Network", "WPA2", "password123")
        qr_string = config.to_qr_string()
        assert "My\\,Network" in qr_string
        assert qr_string == "WIFI:S:My\\,Network;T:WPA2;P:password123;;"

    def test_escape_backslash_in_password(self) -> None:
        """Test that backslash in password is escaped."""
        config = WiFiConfig("MyNetwork", "WPA2", "pass\\word")
        qr_string = config.to_qr_string()
        assert "pass\\\\word" in qr_string

    def test_escape_quote_in_password(self) -> None:
        """Test that quote in password is escaped."""
        config = WiFiConfig("MyNetwork", "WPA2", 'pass"word')
        qr_string = config.to_qr_string()
        assert 'pass\\"word' in qr_string
        assert qr_string == 'WIFI:S:MyNetwork;T:WPA2;P:pass\\"word;;'

    def test_escape_multiple_special_chars(self) -> None:
        """Test escaping multiple special characters."""
        config = WiFiConfig("My;Network:Test", "WPA2", 'pass"word,123')
        qr_string = config.to_qr_string()
        assert "My\\;Network\\:Test" in qr_string
        assert 'pass\\"word\\,123' in qr_string
        assert qr_string == 'WIFI:S:My\\;Network\\:Test;T:WPA2;P:pass\\"word\\,123;;'
