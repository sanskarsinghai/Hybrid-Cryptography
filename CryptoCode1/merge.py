import os

def MergeIn3(n):
    f3=open('CryptoCode\F2\BinfileName11.bin','r')
    f5=open('CryptoCode\F2\BinfileName12.bin','r')
    f6=open('CryptoCode\F2\BinfileName13.bin','r')

    s=''
    for i in f3:
        s+=i

    for i in f5:
        s+=i

    for i in f6:
        s+=i

    s=s.split()
    
    lo='CryptoCode\\decFile\\'+n+'.txt'
    f4=open(lo,'w')
    for i in s:
        a=int(i,2)
        f4.write(chr(a))

    f4.close()
    f3.close()
    f5.close()
    f6.close()

    os.remove("CryptoCode\F2\BinfileName11.bin")
    os.remove("CryptoCode\F2\BinfileName12.bin")
    os.remove("CryptoCode\F2\BinfileName13.bin")