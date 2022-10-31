import os

def MergeIn1(n):
    f3=open('CryptoCode\F2\BinfileName11.bin','rb')
    f5=open('CryptoCode\F2\BinfileName12.bin','rb')
    f6=open('CryptoCode\F2\BinfileName13.bin','rb')

    s=b''
    for i in f3:
        s+=i

    for i in f5:
        s+=i

    for i in f6:
        s+=i

    lo='CryptoCode\\encFile\\'+n+'.bin'

    f4=open(lo,'wb')
    f4.write(s)

    f4.close()
    f3.close()
    f5.close()
    f6.close()

    os.remove("CryptoCode\F2\BinfileName11.bin")
    os.remove("CryptoCode\F2\BinfileName12.bin")
    os.remove("CryptoCode\F2\BinfileName13.bin")