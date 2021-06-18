import qrcode

#qr = qrcode.make('hello world')
#qr.save('myQR.png')

qr = qrcode.QRCode(
    version = 1,
    #error_correction = qrcode.constants.ERROR_CORRECT
    box_size = 14,
    border = 3
)

data = 'abcdefghijklmnopqrstuvwxyz'
qr.add_data(data)
qr.make(fit = True)
img = qr.make_image(fill = 'black', back_color = 'white')
img.save('testing.png')