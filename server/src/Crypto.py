from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad # pad補滿密文(16倍數)
import hashlib

# Formatted: b for bytes/ s for strings
bkey = b"4Mh1NVICHpQYQM9CoCd1Kh7apDZMQrT1"
bIvs = b"CIh3PVp21MrXvXyP"
sKey= "4Mh1NVICHpQYQM9CoCd1Kh7apDZMQrT1"
sIvs = "CIh3PVp21MrXvXyP"

def create_mpg_aes_encrypt(data):
    cipher = AES.new(bkey,AES.MODE_CBC,iv=bIvs)
    ct_bytes = cipher.encrypt(pad(data,AES.block_size))
    return ct_bytes.hex() #回傳16進制

def create_mpg_sha_encrypt(data):
    plain_text = "HashKey=" + sKey + "&" + data + "&HashIV=" + sIvs
    m = hashlib.sha256()
    m.update(plain_text.encode())
    return m.hexdigest().upper()
    
def gen_query_string(data):
    new_string = ""
    for key, value in data.items():
        new_string += key + "=" + value + "&"
    new_string = new_string[:-1]
    return new_string