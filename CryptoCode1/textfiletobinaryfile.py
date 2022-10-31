#-,bullet dots of list, 's or 't
def TxtToBin(n):
    lo='CryptoCode\\UploadF\\'+n
    with open(lo,'r') as txtfile:
        mytextstring = txtfile.read()

    mytextstring = mytextstring.encode('utf-8')

    binarray = ' '.join(format(ch, 'b') for ch in bytearray(mytextstring))

    with open('CryptoCode\F2\BinfileName1.bin', 'w') as binfile:
        binfile.write(binarray)