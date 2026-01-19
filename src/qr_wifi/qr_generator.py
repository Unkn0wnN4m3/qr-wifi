"""QR code generator with configurable options."""

from pathlib import Path
from typing import Literal

import qrcode
from qrcode.image.svg import SvgPathImage

from qr_wifi.exceptions import QRGenerationError

# Type aliases
ErrorCorrection = Literal["L", "M", "Q", "H"]
ImageFormat = Literal["png", "svg"]

# Error correction mapping
ERROR_CORRECTION_MAP = {
    "L": qrcode.ERROR_CORRECT_L,
    "M": qrcode.ERROR_CORRECT_M,
    "Q": qrcode.ERROR_CORRECT_Q,
    "H": qrcode.ERROR_CORRECT_H,
}


class QRGenerator:
    """
    QR code generator with configurable options.

    Attributes:
        error_correction: Error correction level (L, M, Q, H)
        box_size: Size of each box in pixels
        border: Border size in boxes
        format: Output format (png, svg)
        output_dir: Output directory path
    """

    def __init__(
        self,
        error_correction: ErrorCorrection = "L",
        box_size: int = 10,
        border: int = 4,
        format: ImageFormat = "png",
        output_dir: Path | str = ".",
    ) -> None:
        """
        Initialize QR generator with options.

        Args:
            error_correction: Error correction level (default: L)
            box_size: Size of each box in pixels (default: 10)
            border: Border size in boxes (default: 4)
            format: Output format png or svg (default: png)
            output_dir: Output directory (default: current directory)

        Raises:
            QRGenerationError: If configuration is invalid
        """
        if error_correction not in ERROR_CORRECTION_MAP:
            raise QRGenerationError(
                f"Invalid error correction: {error_correction}. "
                f"Valid options: {', '.join(ERROR_CORRECTION_MAP.keys())}"
            )

        if box_size < 1:
            raise QRGenerationError(f"Box size must be >= 1 (got {box_size})")

        if border < 0:
            raise QRGenerationError(f"Border must be >= 0 (got {border})")

        if format not in ["png", "svg"]:
            raise QRGenerationError(
                f"Invalid format: {format}. Valid options: png, svg"
            )

        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border
        self.format = format
        self.output_dir = Path(output_dir)

        # Validate output directory
        if not self.output_dir.exists():
            raise QRGenerationError(
                f"Output directory does not exist: {self.output_dir}"
            )

        if not self.output_dir.is_dir():
            raise QRGenerationError(
                f"Output path is not a directory: {self.output_dir}"
            )

    def generate(self, data: str, filename: str) -> Path:
        """
        Generate QR code and save to file.

        Args:
            data: Data to encode in QR code
            filename: Output filename (without extension)

        Returns:
            Path to generated file

        Raises:
            QRGenerationError: If generation or saving fails
        """
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                error_correction=ERROR_CORRECTION_MAP[self.error_correction],
                box_size=self.box_size,
                border=self.border,
            )

            # Add data and generate
            qr.add_data(data)
            qr.make(fit=True)

            # Generate image based on format
            if self.format == "svg":
                img = qr.make_image(image_factory=SvgPathImage)
            else:
                img = qr.make_image(fill_color="black", back_color="white")

            # Construct output path
            output_path = self.output_dir / f"{filename}.{self.format}"

            # Save image - open file to satisfy type checker
            with open(output_path, "wb") as f:
                img.save(f)  # type: ignore[arg-type]

            return output_path

        except Exception as e:
            raise QRGenerationError(f"Failed to generate QR code: {e}") from e
