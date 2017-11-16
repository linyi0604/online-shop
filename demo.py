import hashlib
'''

原文= ’字符串‘
哈希加密对象 = hashlib.加密算法( 原文.encode('utf-8') )
密文 = 哈希加密对象.hexdigest()     #密文是字符串

'''

password = '123'    #原文
secret = hashlib.sha1(password.encode('utf-8')).hexdigest() #获得密文
print(secret)


secret = hashlib.sha256(password.encode('utf-8')).hexdigest() #获得密文
print(secret)


secret = hashlib.md5(password.encode('utf-8')).hexdigest() #获得密文
print(secret)