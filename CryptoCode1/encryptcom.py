import textfiletobinaryfile as tfb
import breakintothreeparts as b3t
import enc
import mergeenc as mge

print("Encryption process started: -")
print()

tfb.TxtToBin()
b3t.BreakIn3Parts()
k=enc.keygen()
iv=enc.aesenc()
di=enc.desenc()
r=enc.rc4enc()
l=enc.decauth()
enc.stegnoimg(k,iv,di,r,l)

mge.MergeIn1()

print("Encryption process completed")