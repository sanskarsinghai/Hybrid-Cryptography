from stegano import lsb
import os

def stegnoimg(use,imn):   
    print("Stegnographic process is in progress..............")
    
    ilo="CryptoCode\\UploadFdec\\"+imn+".png"

    clear_message = lsb.reveal(ilo)
    s=clear_message.split(' ')
    c=''
    
    for i in range(0,len(s)-1):
        a=int(s[i],2)
        c+=chr(a)
    s=c.split(',')

    lu=list()
    f=0
    for i in s[26:]:
        #owner is also include in lu list
        if i==use:
            f=1
        lu.append(int(i))

    if f==0:
        return [0]

    a=int(s[23])
    d=int(s[24])
    r=int(s[25])

    print("Stegnographic process is completed")

    return [a,d,r]

def DiviIn3(l,n):
    file_number = 0
    print(n)
    
    lo='CryptoCode\\uploadFDec\\'+n+'.bin'

    with open(lo,'rb') as f:
        while file_number<3:
            s=l[file_number]
            chunk = f.read(s)
            with open(('CryptoCode\F2\BinfileName1' + str(file_number+1)+ '.bin'),'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
