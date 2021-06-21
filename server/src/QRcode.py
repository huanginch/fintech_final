import qrcode
from random import randint
import os 
#qr = qrcode.make('hello world')
#qr.save('myQR.png')

def QRcode(QRid):
    qr = qrcode.QRCode(version = 1,box_size = 14,border = 3)
    #a = randint(10000000, 99999999)
    DIR = 'static/'  #要統計的資料夾
    num = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    #data = str(a)
    text = str(num) #要抽換的字
    qr.add_data(QRid)
    qr.make(fit = True)
    img = qr.make_image(fill = 'black', back_color = 'white')
    loc = ('static/test_true.png'.format(text))
    img.save(loc)
    #return data

def qrPath():
    DIR = 'static/'  #要統計的資料夾
    num = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])-1
    text = str(num) #要抽換的字
    loc = ('test{}.png'.format(text))
    return loc
#QRcode()

#print(qrPath())
