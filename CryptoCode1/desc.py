import pyaes
from des import DesKey
from arc4 import ARC4
from stegano import lsb

key=""
t=""
iv=""
di=""
lu=list()
# use=""
o=""

def stegnoimg(use,ilo):
    global t,iv,di,lu,o

    ilo="CryptoCode\\UploadFdec\\"+ilo+".png"

    print("Stegnographic process is in progress..............")
    
    clear_message = lsb.reveal(ilo)
    s=clear_message.split(' ')
    c=''
    
    for i in range(0,len(s)-1):
       a=int(s[i],2)
       c+=chr(a)
    
    s=c.split(',')
   
    o=s[26]
    f=0
    
    for i in s[26:]:
        #owner is also include in lu list
        if i==use:
            f=1
        lu.append(int(i))

    if f==0:
        return "You are no authorized to decypt this file"

    iv=int(s[21])
    di=int(s[22])
    t=s[:21]
    print("Stegnographic process is completed")
    return o

def keygen(l):
    global t,key

    print("Key generation is in progress...........")

    s=""
    for i in range(1,7):
        if type(l[int(t[i])])!=str:
           s+=str(l[int(t[i])])
        else:
           s+=l[int(t[i])]
    d=''
    for i in range(7,len(t)):
        d+=s[int(t[i])]

    d=d[:int(t[0])]+str(l[3])+d[int(t[0]):]

    key=d.encode('utf-8')

    print("Key generated successfully")

def aesdec():
    global key,iv

    daes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))

    f=open('CryptoCode\F2\BinfileName11.bin','rb')
    ciphertext=b''
    
    for i in f:
        ciphertext+=i

    f.close()

    try:
        if len(ciphertext)==0:
           raise Exception
    except Exception:
        print("\nEmpty file cannot be decrypted")
        return "Empty file cannot be decrypted"


    print("Decryption by aes is processing.........")

    try:
        decrypted = daes.decrypt(ciphertext)
        f3=open('CryptoCode\F2\BinfileName11.bin','w')
        f3.write(decrypted.decode('utf-8'))
        f3.close()
    except UnicodeDecodeError as e:
        print("\nInvalid Key for decription")
        return "Invalid Key for decription"

    print("Decryption by aes done")
    return "OK"

def desdec():
    global key,di
    f=open('CryptoCode\F2\BinfileName12.bin','rb')
    e=b''
    
    for i in f:
        e+=i

    f.close()

    try:
        if len(e)==0:
           raise Exception
    except Exception:
        print("\nEmpty file cannot be decrypted")
        return "Empty file cannot be decrypted"

    print("Decryption by des is processing.........")
    
    try:
       key0 = DesKey(key)
       d=key0.decrypt(e) 
       f2=open('CryptoCode\F2\BinfileName12.bin','w')
       f2.write(d.decode('utf-8')[:len(d)-di])
       f2.close()
    except UnicodeDecodeError as e:
        print("\nInvalid Key for decription")
        return "Invalid Key for decription"

    print("Decryption by des done")
    return "OK"

def rc4dec():
    global key
    
    
    f=open('CryptoCode\F2\BinfileName13.bin','rb')
    cipher=b''
    
    for i in f:
        cipher+=i

    f.close()
    
    try:
        if len(cipher)==0:
           raise Exception
    except Exception:
        print("\nEmpty file cannot be decrypted")
        return "Empty file cannot be decrypted"

    print("Decryption by rc4 is processing.........")

    try:
        arc4 = ARC4(key)
        d=arc4.decrypt(cipher)
        f2=open('CryptoCode\F2\BinfileName13.bin','w')
        f2.write(d.decode('utf-8'))
        f2.close()
    except UnicodeDecodeError as e:
        print("\nInvalid Key for decription")
        return "Invalid Key for decription"

    print("Decryption by rc4 done")
    return "OK"
