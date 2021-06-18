import qrcode
from random import randint
#qr = qrcode.make('hello world')
#qr.save('myQR.png')


def QRcode():
    qr = qrcode.QRCode(version = 1,box_size = 14,border = 3)
    a = randint(10000000, 99999999)
    data = str(a)
    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill = 'black', back_color = 'white')
    img.save('testing.png')

