import divideenc as de
import desc
import merge as m
import os

print("\nDecryption process started: -")
print()

ba=os.getcwd()
l=de.stegnoimg()
de.DiviIn3(l)

os.remove(ba+"templates/F2/mergeenc.bin")

desc.stegnoimg()

os.remove(ba+"templates/s1.png")

desc.keygen()
desc.aesdec()
desc.desdec()
desc.rc4dec()

m.MergeIn3()

print("Decryption process completed")