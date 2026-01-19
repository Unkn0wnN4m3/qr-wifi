"""Command-line interface for qr-wifi."""

import argparse
import sys

from qr_wifi.exceptions import QRGenerationError, WiFiConfigError
from qr_wifi.qr_generator import QRGenerator
from qr_wifi.wifi import WiFiConfig


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for CLI.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Generate QR codes for WiFi credentials",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  qr-wifi --ssid "MyNetwork" --security WPA2 --password "mypassword"

  # Open network (no password)
  qr-wifi --ssid "FreeWiFi" --security nopass

  # Hidden network
  qr-wifi --ssid "HiddenNet" --security WPA2 --password "secret" --hidden

  # Custom output options
  qr-wifi --ssid "MyNet" --security WPA --password "pass1234" \\
          --format svg --box-size 15 --output-dir ./qrcodes

  # High error correction for damaged codes
  qr-wifi --ssid "MyNet" --security WPA2 --password "secure" \\
          --error-correction H
        """,
    )

    # Required arguments
    parser.add_argument(
        "--ssid",
        dest="ssid",
        required=True,
        help="WiFi network SSID (1-32 characters)",
    )

    parser.add_argument(
        "--security",
        dest="security",
        required=True,
        choices=["WPA", "WPA2", "WEP", "nopass"],
        help="Security type (WPA, WPA2, WEP, or nopass for open networks)",
    )

    parser.add_argument(
        "--password",
        dest="password",
        default="",
        help="WiFi password (required for WPA/WPA2/WEP, omit for nopass)",
    )

    # Optional WiFi arguments
    parser.add_argument(
        "--hidden",
        dest="hidden",
        action="store_true",
        help="Network is hidden",
    )

    # QR code options
    parser.add_argument(
        "--error-correction",
        dest="error_correction",
        default="L",
        choices=["L", "M", "Q", "H"],
        help=(
            "Error correction level: L (7%%), M (15%%), Q (25%%), H (30%%) - default: L"
        ),
    )

    parser.add_argument(
        "--box-size",
        dest="box_size",
        type=int,
        default=10,
        help="Size of each QR code box in pixels (default: 10)",
    )

    parser.add_argument(
        "--border",
        dest="border",
        type=int,
        default=4,
        help="Border size in boxes (default: 4)",
    )

    # Output options
    parser.add_argument(
        "--format",
        dest="format",
        default="png",
        choices=["png", "svg"],
        help="Output format (default: png)",
    )

    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default=".",
        help="Output directory (default: current directory)",
    )

    parser.add_argument(
        "--output-name",
        dest="output_name",
        help="Output filename without extension (default: SSID)",
    )

    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Create WiFi configuration
        wifi_config = WiFiConfig(
            ssid=args.ssid,
            security=args.security,
            password=args.password,
            hidden=args.hidden,
        )

        # Generate WiFi QR string
        qr_data = wifi_config.to_qr_string()

        # Create QR generator
        qr_generator = QRGenerator(
            error_correction=args.error_correction,
            box_size=args.box_size,
            border=args.border,
            format=args.format,
            output_dir=args.output_dir,
        )

        # Determine output filename
        output_name = args.output_name if args.output_name else args.ssid

        # Generate QR code
        output_path = qr_generator.generate(qr_data, output_name)

        # Success message
        print("QR code generated successfully!")
        print(f"  Network: {args.ssid}")
        print(f"  Security: {args.security}")
        if args.hidden:
            print("  Hidden: Yes")
        print(f"  File: {output_path}")

    except WiFiConfigError as e:
        print("Error: Invalid WiFi configuration", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        sys.exit(1)

    except QRGenerationError as e:
        print("Error: Failed to generate QR code", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print("Error: Unexpected error occurred", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
