# WiFi QR Generator

Generates qr codes to connect to your WiFi network

## Dependencies

- [python3](https://www.python.org/downloads/)
- [pipenv](https://pypi.org/project/pipenv/)
- [qrcode](https://pypi.org/project/qrcode/)

## Usage:

```bash
# 1. Install dependencies within the virtual environment
pipenv install

# 2. Run the virtual environment
pipenv shell

# 3. Run the program
python3 -m qr-wifi --ssid <your_ssid> --security <WEB|WPA> --password <your_pass>
```

