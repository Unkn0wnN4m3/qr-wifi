import argparse

import qrcode

# Inicialize parser
parser = argparse.ArgumentParser(description='Make a QR from WiFi data')

parser.add_argument('--ssid', dest='SSID', required=True)
parser.add_argument('--security',
                    dest='SECURITY',
                    required=True,
                    choices=["WPA", "WEP", "WPA2"])
parser.add_argument('--password', dest='PASSWORD', required=True)

args = parser.parse_args()

# QR initialisation
qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L,
                   box_size=10,
                   border=4)

if __name__ == '__main__':

    ssid, security, password = args.SSID, args.SECURITY, args.PASSWORD
    data = (f'WIFI:S:{ssid};T:{security};P:{password};;')
    print(data)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(f'{ssid}.png')
