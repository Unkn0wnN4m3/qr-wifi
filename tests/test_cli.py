"""Tests for CLI."""

from pathlib import Path
from unittest.mock import patch

import pytest

from qr_wifi.cli import create_parser, main


class TestCreateParser:
    """Test argument parser creation."""

    def test_parser_created(self) -> None:
        """Test that parser is created successfully."""
        parser = create_parser()
        assert parser is not None
        assert parser.description is not None

    def test_required_arguments(self) -> None:
        """Test that required arguments are enforced."""
        parser = create_parser()

        # Missing all required arguments
        with pytest.raises(SystemExit):
            parser.parse_args([])

        # Missing password is OK for nopass
        args = parser.parse_args(["--ssid", "Test", "--security", "nopass"])
        assert args.ssid == "Test"
        assert args.security == "nopass"

    def test_parse_basic_arguments(self) -> None:
        """Test parsing basic arguments."""
        parser = create_parser()
        args = parser.parse_args(
            ["--ssid", "MyNetwork", "--security", "WPA2", "--password", "password123"]
        )

        assert args.ssid == "MyNetwork"
        assert args.security == "WPA2"
        assert args.password == "password123"
        assert args.hidden is False

    def test_parse_hidden_flag(self) -> None:
        """Test parsing hidden flag."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "--ssid",
                "Hidden",
                "--security",
                "WPA2",
                "--password",
                "secret",
                "--hidden",
            ]
        )

        assert args.hidden is True

    def test_parse_error_correction(self) -> None:
        """Test parsing error correction levels."""
        parser = create_parser()

        for level in ["L", "M", "Q", "H"]:
            args = parser.parse_args(
                [
                    "--ssid",
                    "Test",
                    "--security",
                    "WPA2",
                    "--password",
                    "pass",
                    "--error-correction",
                    level,
                ]
            )
            assert args.error_correction == level

    def test_parse_box_size(self) -> None:
        """Test parsing box size."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "--ssid",
                "Test",
                "--security",
                "WPA2",
                "--password",
                "pass",
                "--box-size",
                "20",
            ]
        )

        assert args.box_size == 20

    def test_parse_border(self) -> None:
        """Test parsing border size."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "--ssid",
                "Test",
                "--security",
                "WPA2",
                "--password",
                "pass",
                "--border",
                "2",
            ]
        )

        assert args.border == 2

    def test_parse_format(self) -> None:
        """Test parsing output format."""
        parser = create_parser()

        for fmt in ["png", "svg"]:
            args = parser.parse_args(
                [
                    "--ssid",
                    "Test",
                    "--security",
                    "WPA2",
                    "--password",
                    "pass",
                    "--format",
                    fmt,
                ]
            )
            assert args.format == fmt

    def test_parse_output_dir(self) -> None:
        """Test parsing output directory."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "--ssid",
                "Test",
                "--security",
                "WPA2",
                "--password",
                "pass",
                "--output-dir",
                "./output",
            ]
        )

        assert args.output_dir == "./output"

    def test_parse_output_name(self) -> None:
        """Test parsing output name."""
        parser = create_parser()
        args = parser.parse_args(
            [
                "--ssid",
                "Test",
                "--security",
                "WPA2",
                "--password",
                "pass",
                "--output-name",
                "custom_name",
            ]
        )

        assert args.output_name == "custom_name"

    def test_default_values(self) -> None:
        """Test that default values are set correctly."""
        parser = create_parser()
        args = parser.parse_args(
            ["--ssid", "Test", "--security", "WPA2", "--password", "pass"]
        )

        assert args.password == "pass"
        assert args.hidden is False
        assert args.error_correction == "L"
        assert args.box_size == 10
        assert args.border == 4
        assert args.format == "png"
        assert args.output_dir == "."
        assert args.output_name is None


class TestMainFunction:
    """Test main CLI function."""

    def test_main_success(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test successful QR code generation via CLI."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "TestNet",
            "--security",
            "WPA2",
            "--password",
            "testpass123",
            "--output-dir",
            str(tmp_path),
        ]

        with patch("sys.argv", test_args):
            main()

        # Check output
        captured = capsys.readouterr()
        assert "QR code generated successfully!" in captured.out
        assert "TestNet" in captured.out
        assert "WPA2" in captured.out

        # Check file was created
        output_file = tmp_path / "TestNet.png"
        assert output_file.exists()

    def test_main_with_custom_output_name(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test CLI with custom output name."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "TestNet",
            "--security",
            "WPA2",
            "--password",
            "password123",
            "--output-dir",
            str(tmp_path),
            "--output-name",
            "custom",
        ]

        with patch("sys.argv", test_args):
            main()

        # Check file was created with custom name
        output_file = tmp_path / "custom.png"
        assert output_file.exists()

    def test_main_svg_format(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test CLI with SVG format."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "TestNet",
            "--security",
            "WPA2",
            "--password",
            "password123",
            "--output-dir",
            str(tmp_path),
            "--format",
            "svg",
        ]

        with patch("sys.argv", test_args):
            main()

        # Check SVG file was created
        output_file = tmp_path / "TestNet.svg"
        assert output_file.exists()

    def test_main_open_network(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test CLI with open network."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "OpenNet",
            "--security",
            "nopass",
            "--output-dir",
            str(tmp_path),
        ]

        with patch("sys.argv", test_args):
            main()

        captured = capsys.readouterr()
        assert "nopass" in captured.out

        output_file = tmp_path / "OpenNet.png"
        assert output_file.exists()

    def test_main_hidden_network(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test CLI with hidden network."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "HiddenNet",
            "--security",
            "WPA2",
            "--password",
            "secretpass",
            "--hidden",
            "--output-dir",
            str(tmp_path),
        ]

        with patch("sys.argv", test_args):
            main()

        captured = capsys.readouterr()
        assert "Hidden: Yes" in captured.out

    def test_main_invalid_ssid(self, capsys: pytest.CaptureFixture) -> None:
        """Test CLI with invalid SSID."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "",
            "--security",
            "WPA2",
            "--password",
            "pass",
        ]

        with patch("sys.argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_main_invalid_password(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test CLI with invalid password."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "TestNet",
            "--security",
            "WPA2",
            "--password",
            "short",
            "--output-dir",
            str(tmp_path),
        ]

        with patch("sys.argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error" in captured.err
        assert "Invalid WiFi configuration" in captured.err

    def test_main_nonexistent_output_dir(self, capsys: pytest.CaptureFixture) -> None:
        """Test CLI with nonexistent output directory."""
        test_args = [
            "qr-wifi",
            "--ssid",
            "TestNet",
            "--security",
            "WPA2",
            "--password",
            "password123",
            "--output-dir",
            "/nonexistent/path",
        ]

        with patch("sys.argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error" in captured.err
        assert "Failed to generate QR code" in captured.err
