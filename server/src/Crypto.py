from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad # pad補滿密文(16倍數)
import hashlib

# Formatted: b for bytes/ s for strings
bkey = b"Zsw1hcMSsUXaYD6KkNXp51CYPownOs2Q"
bIvs = b"C4eSt2R0mnZRadfP"
sKey= "Zsw1hcMSsUXaYD6KkNXp51CYPownOs2Q"
sIvs = "C4eSt2R0mnZRadfP"

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