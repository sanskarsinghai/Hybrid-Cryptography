import divideenc as de
import desc
import merge as m
import os

print("\nDecryption process started: -")
print()

l=de.stegnoimg()
de.DiviIn3(l)

os.remove("templates/F2/mergeenc.bin")

desc.stegnoimg()

os.remove("templates/s1.png")

desc.keygen()
desc.aesdec()
desc.desdec()
desc.rc4dec()

m.MergeIn3()

print("Decryption process completed")