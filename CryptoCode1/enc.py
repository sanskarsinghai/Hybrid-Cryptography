from telnetlib import PRAGMA_HEARTBEAT
from turtle import pen
import pyaes, secrets
from des import DesKey
from arc4 import ARC4
from stegano import lsb
import random as ra

# key = token_bytes(16)
key = ''
def keygen(l):
    global key    
    print("Key generation is in progress...........")
    v=list(range(0,6))
    s=''
    t=''
    for _ in range(0,5):
       a=ra.choice(v)
       v.remove(a)
       t+=str(a)+','
       if type(l[a])!=str:
           s+=str(l[a])
       else:
           s+=l[a]

    if type(l[v[0]])!=str:
        s+=str(l[v[0]])
    else:
        s+=l[v[0]]
    t+=str(v[0])+','
    
    p=ra.choice(range(0,14))
    tok=""
    for _ in range(0,14):
       a=ra.choice(range(0,len(s)))
       t+=str(a)+','
       key+=s[a]
       tok+=str(ord(s[a]))

    # if p=='l':
    #     key+=str(l[3])
    # else:
    #     key=str(l[3])+key

    
    key=key[:p]+str(l[3])+key[p:]

    t=t[:len(t)-1]
    t=str(p)+','+t

    for i in str(p):
        tok+=str(ord(i))
    
    
    bp=tok.encode('utf-8')
    f=''
    for i in bytearray(bp):
        f+=format(i,'b')

    key=key.encode('utf-8')
    
    print("Key generated successfully")

    return [t,f]

def aesenc():
    global key
    iv = secrets.randbits(64)
    
    f=open("CryptoCode\F2\BinfileName11.bin")
    plaintext=''
    for i in f:
        plaintext+=i
    f.close()

    try:
        if len(plaintext)==0:
           raise Exception
    except Exception:
        print("\nEmpty file cannot be encrypted")
        exit()
    
    print("Encryption by aes is processing.........")

    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(plaintext)

    f2=open('CryptoCode\F2\BinfileName11.bin','wb')
    f2.write(ciphertext)

    print("Encryption by aes done")
    l=[iv,len(ciphertext)]
    return l

def desenc():
    global key
    
    f=open("CryptoCode\F2\BinfileName12.bin")

    s=''
    for i in f:
        s+=i
    f.close()
    
    try:
        if len(s)==0:
           raise Exception
    except Exception:
        print("\nEmpty file cannot be decrypted")
        exit()
    
    print("Encryption by des is processing.........")

    key0 = DesKey(key)
    e=key0.encrypt(s.encode('utf-8'),padding=True)

    f2=open('CryptoCode\F2\BinfileName12.bin','wb')
    f2.write(e)
    
    di=len(e)-len(s)

    print("Encryption by des done")
    l=[di,len(e)]
    return l

def rc4enc():
    global key
    
    f=open("CryptoCode\F2\BinfileName13.bin")

    s=''
    for i in f:
        s+=i
    f.close()
    
    try:
        if len(s)==0:
           raise Exception
    except Exception:
        print("\nEmpty file cannot be decrypted")
        exit()

    print("Encryption by rc4 is processing.........")

    arc4 = ARC4(key)
    cipher = arc4.encrypt(s.encode('utf-8'))

    f2=open('CryptoCode\F2\BinfileName13.bin','wb')
    f2.write(cipher)
    
    print("Encryption by rc4 done")
    return len(cipher)

def decauth(o,de):
    print("Process of detecting user who can decrypt the file is in progress...........\n")
    
    l=str(o)+","
    for i in de:
        l+=str(i)+","

    print("Process of saving user who can decrypt the file is recorded successfully")
    return l[:len(l)-1]

def stegnoimg(k,iv,di,r,l,imn,nimn):
    print("Stegnographic process is in progress..............")
    s=k+","+str(iv[0])+","+str(di[0])+","+str(iv[1])+","+str(di[1])+","+str(r)+","+l
    s=s.encode("utf-8")

    c=''
    for i in s:
        c+=format(i,'b')+' '
    rk=c

    lo="CryptoCode\\UploadF\\"+imn

    secret = lsb.hide(lo,c)
    
    loc="CryptoCode\\encFile\\"+nimn+".png"
    secret.save(loc)
   
    print("Stegnographic process is completed")
    return rk