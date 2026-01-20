# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-20

### Added

#### Core Features

- WiFi QR code generation with comprehensive validation
- Support for multiple security types: WPA, WPA2, WEP, and open networks
- Input validation for SSID length (1-32 characters) and password requirements
- Multiple output formats: PNG and SVG
- Configurable QR code options:
  - Error correction levels (L, M, Q, H)
  - Box size customization
  - Border size adjustment
- Special character escaping for WiFi configuration strings
- Hidden network support

#### Command-Line Interface

- Intuitive CLI with argparse
- Required arguments: `--ssid`, `--security`, `--password`
- Optional arguments: `--hidden`, `--error-correction`, `--box-size`, `--border`
- Output options: `--format`, `--output-dir`, `--output-name`
- Clear error messages for invalid configurations

#### Programmatic API

- `WiFiConfig` class for WiFi configuration management
- `QRGenerator` class for QR code generation
- `to_qr_string()` method for generating WiFi configuration strings
- Type-safe API with proper type hints
- Custom exceptions for error handling

#### Testing

- Comprehensive test suite with 68 tests
- 100% coverage of core functionality
- Tests for WiFi configuration validation
- Tests for QR code generation
- Tests for CLI functionality
- Pytest configuration with coverage reporting

#### Development Tools

- Type checking with basedpyright
- Code linting and formatting with ruff
- Pre-commit hooks for code quality enforcement
- Automated checks for:
  - Trailing whitespace
  - End of file fixing
  - YAML/TOML syntax validation
  - Python linting and formatting
  - Markdown linting
  - Type checking

#### Documentation

- Comprehensive README with:
  - Installation instructions (uv and pip)
  - Usage examples (basic and advanced)
  - Command-line options reference
  - Password requirements for each security type
  - Development setup guide
  - Project structure overview
  - Programmatic usage examples
  - Contributing guidelines
- Well-documented code with docstrings
- Type hints throughout the codebase

### Fixed

- Type errors in test suite using proper type casting
- Markdown formatting issues in README
- Git tracking of `__pycache__` directories

### Changed

- Updated README note to mention vibe coding refactor
- Improved `.gitignore` to ignore all `__pycache__` subdirectories

### Development

- Project setup with `uv` for dependency management
- Python 3.12+ requirement
- Development dependencies properly organized
- CI/CD ready configuration

## Project Information

**Repository:** https://github.com/Unkn0wnN4m3/qr-wifi  
**Author:** Unkn0wnN4m3  
**License:** Open Source

[1.0.0]: https://github.com/Unkn0wnN4m3/qr-wifi/releases/tag/v1.0.0
