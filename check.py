import os

ba=os.getcwd()
f1=open(ba+'/templates/UploadF/data.txt')
f2=open(ba+'/templates/UploadF/origin.txt')

s=''
for i in f1:
    s+=i

t=''
for i in f2:
    t+=i
f=0
for i in range(len(s)):
    if s[i]!=t[i]:
        print(False)
        f=1
        print(i,s[i],t[i])

if f==0:
    print("Process Successfully completed")      