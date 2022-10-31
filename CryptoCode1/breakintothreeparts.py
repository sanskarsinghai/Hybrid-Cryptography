import os

def BreakIn3Parts():

    file_stat = os.stat('CryptoCode\F2\BinfileName1.bin')
    a = file_stat.st_size+1

    CHUNK_SIZE = a//3
    l=[0,0,0]
    if a%3!=0:
        s=a/3-a//3
        if s==0.333:
            l[2]=1
        else:
            l[1]=1
            l[2]=1
            
    file_number = 0
    with open('CryptoCode\F2\BinfileName1.bin') as f:
        while file_number<3:
            s=CHUNK_SIZE+l[file_number]
            chunk = f.read(s)
            with open(('CryptoCode\F2\BinfileName1' + str(file_number+1)+ '.bin'),'w') as chunk_file:
                chunk_file.write(str(chunk))
            file_number += 1
            
    os.remove("CryptoCode\F2\BinfileName1.bin")