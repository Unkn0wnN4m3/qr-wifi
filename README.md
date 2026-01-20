# qr-wifi

Generate QR codes for WiFi credentials with validation and configurable options.

> **Note:** This project was refactored using vibe coding.

## Features

- 🔐 **Secure WiFi QR codes** - WPA, WPA2, WEP, and open networks
- ✅ **Input validation** - Validates SSID, password, and security types
- 🎨 **Multiple formats** - Generate PNG or SVG QR codes
- ⚙️ **Configurable** - Customize error correction, box size, and border
- 🔒 **Special character handling** - Automatically escapes special characters
- 📱 **Hidden network support** - Option for hidden SSIDs
- 🧪 **Well tested** - Comprehensive test suite with pytest

## Installation

Using `uv` (recommended):

```bash
uv sync
```

Or install with pip:

```bash
pip install -e .
```

## Usage

### Basic Usage

Generate a QR code for a WPA2 network:

```bash
qr-wifi --ssid "MyNetwork" --security WPA2 --password "mypassword"
```

This creates a `MyNetwork.png` file in the current directory.

### Open Network (No Password)

```bash
qr-wifi --ssid "FreeWiFi" --security nopass
```

### Hidden Network

```bash
qr-wifi --ssid "HiddenNet" --security WPA2 --password "secret" --hidden
```

### Custom Output Options

Generate an SVG with custom sizing:

```bash
qr-wifi --ssid "MyNet" --security WPA --password "pass1234" \
        --format svg --box-size 15 --output-dir ./qrcodes
```

### High Error Correction

For QR codes that might be damaged or dirty:

```bash
qr-wifi --ssid "MyNet" --security WPA2 --password "secure" \
        --error-correction H
```

## Command-Line Options

### Required Arguments

- `--ssid SSID` - WiFi network SSID (1-32 characters)
- `--security TYPE` - Security type: `WPA`, `WPA2`, `WEP`, or `nopass`
- `--password PASSWORD` - WiFi password (required for WPA/WPA2/WEP)

### Optional WiFi Arguments

- `--hidden` - Mark network as hidden

### QR Code Options

- `--error-correction LEVEL` - Error correction level:
  - `L` - Low (7% recovery) - default
  - `M` - Medium (15% recovery)
  - `Q` - Quartile (25% recovery)
  - `H` - High (30% recovery)
- `--box-size SIZE` - Size of each QR box in pixels (default: 10)
- `--border SIZE` - Border size in boxes (default: 4)

### Output Options

- `--format FORMAT` - Output format: `png` or `svg` (default: png)
- `--output-dir DIR` - Output directory (default: current directory)
- `--output-name NAME` - Output filename without extension (default: SSID)

## Password Requirements

### WPA/WPA2

- 8-63 characters
- Can contain any characters

### WEP

- Must be hexadecimal (0-9, A-F)
- Must be 10, 26, or 58 characters long

### Open Networks (nopass)

- No password required

## Development

### Setup

Install development dependencies:

```bash
uv sync
```

### Running Tests

Run all tests:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=qr_wifi --cov-report=html
```

### Type Checking

```bash
uv run basedpyright
```

### Linting

Check code style:

```bash
uv run ruff check
```

Format code:

```bash
uv run ruff format
```

## Project Structure

```text
qr-wifi/
├── src/
│   └── qr_wifi/
│       ├── __init__.py       # Public API
│       ├── cli.py            # Command-line interface
│       ├── wifi.py           # WiFi configuration with validation
│       ├── qr_generator.py   # QR code generation
│       └── exceptions.py     # Custom exceptions
├── tests/
│   ├── test_wifi.py          # WiFi configuration tests
│   ├── test_qr_generator.py  # QR generator tests
│   └── test_cli.py           # CLI tests
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Programmatic Usage

You can also use qr-wifi as a library:

```python
from qr_wifi import WiFiConfig, QRGenerator

# Create WiFi configuration
config = WiFiConfig(
    ssid="MyNetwork",
    security="WPA2",
    password="mypassword",
    hidden=False
)

# Generate QR string
qr_data = config.to_qr_string()

# Create QR code
generator = QRGenerator(
    error_correction="L",
    box_size=10,
    border=4,
    format="png",
    output_dir="."
)

# Generate and save
output_path = generator.generate(qr_data, "MyNetwork")
print(f"QR code saved to: {output_path}")
```

## Error Handling

The tool provides clear error messages for common issues:

- Invalid SSID (empty or too long)
- Invalid password (too short, too long, or wrong format)
- Unsupported security type
- Nonexistent output directory

## License

This project is open source. See the license file for details.

## Contributing

Contributions are welcome! Please ensure:

1. Tests pass: `uv run pytest`
2. Type checks pass: `uv run basedpyright`
3. Code is formatted: `uv run ruff format`
4. Linting passes: `uv run ruff check`

## Author

Unkn0wnN4m3
