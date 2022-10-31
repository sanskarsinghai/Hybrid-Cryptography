import divideenc as de
import desc
import merge as m
import os

print("\nDecryption process started: -")
print()

l=de.stegnoimg()
de.DiviIn3(l)

os.remove("CryptoCode\F2\mergeenc.bin")

desc.stegnoimg()

os.remove("CryptoCode\s1.png")

desc.keygen()
desc.aesdec()
desc.desdec()
desc.rc4dec()

m.MergeIn3()

print("Decryption process completed")