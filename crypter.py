# -*- coding: utf-8 -*-
"""
@Time ： 2021/10/21 13:52
@Auth ： apecode
@File ：crypter.py
@IDE ：PyCharm
@Blog：https://liiuyangxiong.cn

"""

"""
表单加密来自：https://github.com/Sricor/Yiban/blob/main/crypter.py
"""

from Crypto.Cipher import AES
from base64 import b64encode, b64decode


def aes_encrypt(aes_key, aes_iv, data):
    """
    aes_key: 密钥
    aes_iv: iv
    提交表单加密
    """
    aes_key = bytes(aes_key, 'utf-8')
    aes_iv = bytes(aes_iv, 'utf-8')
    data = bytes(data, 'utf-8')
    data = aes_pkcs7padding(data)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = b64encode(cipher.encrypt(data))
    return b64encode(encrypted)


def aes_decrypt(aes_key, aes_iv, data):
    """
    aes_key: 密钥
    aes_iv: iv
    提交表单解密
    """
    aes_key = bytes(aes_key, 'utf-8')
    aes_iv = bytes(aes_iv, 'utf-8')
    data = b64decode(b64decode(data))
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    decrypted = cipher.decrypt(data)
    return decrypted.decode('utf-8')


def aes_pkcs7padding(data):
    bs = AES.block_size
    padding = bs - len(data) % bs
    padding_text = bytes(chr(padding) * padding, 'utf-8')
    return data + padding_text


def aes_pkcs7unpadding(data):
    lengt = len(data)
    unpadding = ord(data[lengt - 1])
    return data[0:lengt-unpadding]
