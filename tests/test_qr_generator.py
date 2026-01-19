"""Tests for QR code generator."""

from pathlib import Path

import pytest

from qr_wifi.exceptions import QRGenerationError
from qr_wifi.qr_generator import QRGenerator


class TestQRGeneratorInit:
    """Test QRGenerator initialization."""

    def test_default_config(self, tmp_path: Path) -> None:
        """Test default configuration."""
        generator = QRGenerator(output_dir=tmp_path)
        assert generator.error_correction == "L"
        assert generator.box_size == 10
        assert generator.border == 4
        assert generator.format == "png"
        assert generator.output_dir == tmp_path

    def test_custom_error_correction(self, tmp_path: Path) -> None:
        """Test custom error correction levels."""
        for level in ["L", "M", "Q", "H"]:
            generator = QRGenerator(error_correction=level, output_dir=tmp_path)
            assert generator.error_correction == level

    def test_invalid_error_correction(self, tmp_path: Path) -> None:
        """Test that invalid error correction raises error."""
        with pytest.raises(QRGenerationError, match="Invalid error correction"):
            QRGenerator(error_correction="X", output_dir=tmp_path)  # type: ignore

    def test_custom_box_size(self, tmp_path: Path) -> None:
        """Test custom box size."""
        generator = QRGenerator(box_size=20, output_dir=tmp_path)
        assert generator.box_size == 20

    def test_invalid_box_size(self, tmp_path: Path) -> None:
        """Test that box size less than 1 raises error."""
        with pytest.raises(QRGenerationError, match="Box size must be"):
            QRGenerator(box_size=0, output_dir=tmp_path)

    def test_custom_border(self, tmp_path: Path) -> None:
        """Test custom border size."""
        generator = QRGenerator(border=2, output_dir=tmp_path)
        assert generator.border == 2

    def test_invalid_border(self, tmp_path: Path) -> None:
        """Test that negative border raises error."""
        with pytest.raises(QRGenerationError, match="Border must be"):
            QRGenerator(border=-1, output_dir=tmp_path)

    def test_svg_format(self, tmp_path: Path) -> None:
        """Test SVG format."""
        generator = QRGenerator(format="svg", output_dir=tmp_path)
        assert generator.format == "svg"

    def test_invalid_format(self, tmp_path: Path) -> None:
        """Test that invalid format raises error."""
        with pytest.raises(QRGenerationError, match="Invalid format"):
            QRGenerator(format="jpg", output_dir=tmp_path)  # type: ignore

    def test_nonexistent_output_dir(self) -> None:
        """Test that nonexistent output directory raises error."""
        with pytest.raises(QRGenerationError, match="does not exist"):
            QRGenerator(output_dir="/nonexistent/path")

    def test_output_dir_is_file(self, tmp_path: Path) -> None:
        """Test that output directory cannot be a file."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test")

        with pytest.raises(QRGenerationError, match="not a directory"):
            QRGenerator(output_dir=file_path)


class TestQRGeneratorGenerate:
    """Test QR code generation."""

    def test_generate_png(self, tmp_path: Path) -> None:
        """Test generating PNG QR code."""
        generator = QRGenerator(output_dir=tmp_path)
        data = "WIFI:S:TestNet;T:WPA2;P:password123;;"

        output_path = generator.generate(data, "test")

        assert output_path.exists()
        assert output_path.name == "test.png"
        assert output_path.parent == tmp_path
        assert output_path.stat().st_size > 0

    def test_generate_svg(self, tmp_path: Path) -> None:
        """Test generating SVG QR code."""
        generator = QRGenerator(format="svg", output_dir=tmp_path)
        data = "WIFI:S:TestNet;T:WPA2;P:password123;;"

        output_path = generator.generate(data, "test")

        assert output_path.exists()
        assert output_path.name == "test.svg"
        assert output_path.parent == tmp_path
        assert output_path.stat().st_size > 0

    def test_generate_custom_box_size(self, tmp_path: Path) -> None:
        """Test generating with custom box size."""
        generator_small = QRGenerator(box_size=5, output_dir=tmp_path)
        generator_large = QRGenerator(box_size=20, output_dir=tmp_path)
        data = "WIFI:S:TestNet;T:WPA2;P:password123;;"

        output_small = generator_small.generate(data, "small")
        output_large = generator_large.generate(data, "large")

        assert output_small.exists()
        assert output_large.exists()
        # Larger box size should produce larger file
        assert output_large.stat().st_size > output_small.stat().st_size

    def test_generate_custom_error_correction(self, tmp_path: Path) -> None:
        """Test generating with different error correction levels."""
        for level in ["L", "M", "Q", "H"]:
            generator = QRGenerator(error_correction=level, output_dir=tmp_path)
            data = "WIFI:S:TestNet;T:WPA2;P:password123;;"

            output_path = generator.generate(data, f"qr_{level}")

            assert output_path.exists()
            assert output_path.name == f"qr_{level}.png"

    def test_generate_overwrites_existing(self, tmp_path: Path) -> None:
        """Test that generating overwrites existing file."""
        generator = QRGenerator(output_dir=tmp_path)
        data = "WIFI:S:TestNet;T:WPA2;P:password123;;"

        # Generate first time
        output1 = generator.generate(data, "test")

        # Generate again with different data
        data2 = "WIFI:S:DifferentNet;T:WPA2;P:differentpass;;"
        output2 = generator.generate(data2, "test")

        assert output1 == output2
        assert output2.exists()
        # File should exist and potentially have different size
        size2 = output2.stat().st_size
        assert size2 > 0

    def test_generate_empty_data(self, tmp_path: Path) -> None:
        """Test generating with empty data still works."""
        generator = QRGenerator(output_dir=tmp_path)

        output_path = generator.generate("", "empty")

        assert output_path.exists()

    def test_generate_long_data(self, tmp_path: Path) -> None:
        """Test generating with long data."""
        generator = QRGenerator(output_dir=tmp_path)
        # Create long WiFi string with long SSID and password
        data = "WIFI:S:" + "A" * 32 + ";T:WPA2;P:" + "B" * 63 + ";;"

        output_path = generator.generate(data, "long")

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_generate_special_filename(self, tmp_path: Path) -> None:
        """Test generating with special characters in filename."""
        generator = QRGenerator(output_dir=tmp_path)
        data = "WIFI:S:TestNet;T:WPA2;P:password123;;"

        # Use filename with spaces and special chars
        output_path = generator.generate(data, "my_test-file")

        assert output_path.exists()
        assert output_path.name == "my_test-file.png"
