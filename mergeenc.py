import os

def MergeIn1(n):    
    ba=os.getcwd()
    f3=open(ba+'/templates/F2/BinfileName11.bin','rb')
    f5=open(ba+'/templates/F2/BinfileName12.bin','rb')
    f6=open(ba+'/templates/F2/BinfileName13.bin','rb')

    s=b''
    for i in f3:
        s+=i

    for i in f5:
        s+=i

    for i in f6:
        s+=i

    lo=ba+'/templates/encFile/'+n+'.bin'

    f4=open(lo,'wb')
    f4.write(s)

    f4.close()
    f3.close()
    f5.close()
    f6.close()

    os.remove(ba+"/templates/F2/BinfileName11.bin")
    os.remove(ba+"/templates/F2/BinfileName12.bin")
    os.remove(ba+"/templates/F2/BinfileName13.bin")