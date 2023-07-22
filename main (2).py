import random
#Declaring Permutation table(P), Substitution table(Q) and binary to decimal table
pi_Q = {0: 9, 1: 14, 2: 5, 3: 6, 4: 10, 5: 2, 6: 3, 7: 12, 8: 15, 9: 0, 10: 4, 11: 13, 12: 7, 13: 11, 14: 1, 15: 8}
pi_P = {0: 3, 1: 15, 2: 14, 3: 0, 4: 5, 5: 4, 6: 11, 7: 12, 8: 13, 9: 10, 10: 9, 11: 6, 12: 7, 13: 8, 14: 2, 15: 1,}
bin_to_dec = {0: "0000", 1: "0001", 2: "0010", 3: "0011", 4: "0100", 5: "0101", 6: "0110", 7: "0111", 8: "1000", 9: "1001", 10: "1010", 11: "1011", 12: "1100", 13: "1101", 14: "1110", 15: "1111"}
#Function for initial key generation
#input: -None- output:128 bit Encryption and decryption keys
def kcbingenerator():
    l = []
    for i in range(10):
        l.append(str(i))
    for i in range(97, 103):
        l.append(chr(i))
    key = ""
    for i in range(32):
        a = random.randint(0, len(l)-1)
        key += l[a]
    print("Random cipher key : ", key)
    l0 = key[:16]               # L0
    r0 = key[16:]               # R0
    hex_to_bin = {'0': "0000", '1': "0001", '2': "0010", '3': "0011", '4': "0100", '5': "0101", '6': "0110", '7': "0111", '8': "1000", '9': "1001", 'a': "1010", 'b': "1011", 'c': "1100", 'd': "1101", 'e': "1110", 'f': "1111"}
    bin_to_hex = {"0000": '0', "0001": '1', "0010": '2', "0011": '3', "0100": '4', "0101": '5', "0110": '6', "0111": '7', "1000": '8', "1001": '9', "1010": 'a', "1011": 'b', "1100": 'c', "1101": 'd', "1110": 'e', "1111": 'f'}
    binkey = ''                 # Binary Cipher Key
    for i in r0:
        binkey += hex_to_bin[i]
    crr = ""
    crl = ""
    for i in binkey:
        if(i == '0'):
            crr += '1'
            crl += '1'
        else:
            crr += '0'
            crl += '1'
    Kcbin = binkey+crr          # Kc Encryption Key in Binary
    Ksbin = crl+crr             # Ks Decryption Key to be sent Binary
    Kc = ""                     # Kc Hexadecimal
    for i in range(0, len(Kcbin), 4):
        b = Kcbin[i:i+4]
        Kc += bin_to_hex[b]
    Ks = ""  # Ks hexadecimal
    for i in range(0, len(Ksbin), 4):
        b = Ksbin[i:i+4]
        Ks += bin_to_hex[b]
    return Kcbin,Ksbin
#A function for xor operation of 4 binary strings
#input:4 32-bit binary strings output:Xor-ed 32-bit binary string
def xor(a,b,c,d):
    r=''
    for i in range(32):
        r+=str(int(a[i])^int(b[i])^int(c[i])^int(d[i]))
    return r
#A function for xor operation of 2 binary strings
#input:2 64-bit binary strings output:Xor-ed 64-bit binary string
def xor2(a,b):
    r=''
    for i in range(64):
        r+=str(int(a[i])^int(b[i]))
    return r
#A function for performing shift rows operation on a given binary string
#input:16 bit binary string output:16-bit binary string with left circular shift on every 4 bits
def shiftrows(l):
    bigst = ''
    for i in range(0, 16, 4):
        temp = l[i]
        j = i+1
        st = ''
        while(j < i+4):
            st = st+l[j]
            j = j+1
        st = st+temp
        bigst = bigst+st
    return bigst
#A function for performing permutation on given binary string using P table
#input:4-bit binary string, Complete binary string, the index of the 4-bit binary string output:binary string after performing permutation
def permutation(pt, k,j):
    re = ""
    for i in range(j,j+4):
        re += k[pi_P[i]]
    return re
#A function for performing substitution on the given binary using Q table
#input:binary string output:binary string after performing substitution using the Q table
def substitution(pt):
    re = ""
    k = int(pt, 2)
    re += bin_to_dec[pi_Q[k]]
    return re
#A function involving 3 iterations with a combination of substitution and permutation operations
#input:16-bit binary string output:16-bit binary string after performing subtitution and permutation operation
def Ffunction(p):
    for i in range(3):
        res=''
        for j in range(0,16,4):

            if(j%8==0):
                if(i!=1):
                    res+=permutation(p[j:j+4],p,j)
                else:
                    res+=substitution(p[j:j+4])
            else:
                if(i!=1):
                    res+=substitution(p[j:j+4])
                else:
                    res+=permutation(p[j:j+4],p,j)
        t1 = res[0:4]
        t2 = res[4:8]
        t3 = res[8:12]
        t4 = res[12:16]
        if(i!=2):
            T11 = t1[:2]+t2[:2]
            T21 = t1[2:]+t3[:2]
            T31 = t2[2:]+t4[:2]
            T41 = t3[2:]+t4[2:]
            p = T11+T21+T31+T41
        else:
            p = res
    return p
#A function for performing railfence operation
#input:Binary string on which railfence is to be performed output:binary string with same length as the input string after performing railfence cipher with key length 2
def railfence(text):
    key=2
    fence = [[None] * len(text) for i in range(key)]
    rails = list(range(key - 1)) + list(range(key - 1, 0, -1))
        # Write the characters in the fence pattern
    for i, char in enumerate(text):
        fence[rails[i % len(rails)]][i] = char
        # Read off the fence pattern
    result = []
    for rail in fence:
        result += [char for char in rail if char is not None]
    return ''.join(result)
#A function to perform transposition cipher by converting the input to matrix and transpose it. 
#16-bit binary string output:binary string after performing transpose and converting it to string
def transposition(p):
    matrix = [[p[i+j*4] for i in range(4)] for j in range(4)]
    trans=''
    for i in range(4):
        l=''
        for j in range(4):
            l+=matrix[j][i]
        trans+=l
    return trans
#A function to produce 5 round keys for a given 128 bit key (both for encryption and decryption)
#input:128-bit key in binary string format output:List of 5 binary strings each 32-bit long
def keygenerator(kc):
    keys = []
    for i in range(0, 128, 16):
        k = kc[i:i+16]
        keys.append(k)
    
    for i in range(len(keys)):
        keys[i] = shiftrows(keys[i])
    
    ffunced = []
    for i in keys:
        ffunced.append(Ffunction(i))
    
    tranrail=[]
    for i in range(8):
        if(i in [1,2,5,6]):
            tranrail.append(railfence(ffunced[i]))
        else:
            tranrail.append(transposition(ffunced[i]))
    FinalKeys=[]
    for i in range(0,8,2):
        l=''
        l=tranrail[i]+tranrail[i+1]
        FinalKeys.append(l)
    key5 = xor(FinalKeys[0],FinalKeys[1],FinalKeys[2],FinalKeys[3])
    FinalKeys.append(key5)
    return FinalKeys
#A function for generating initial key generation for decryption key
#input: 128-bit decryption key produced by initial key generationn function output:128-bit key binary string used for key generation process 
def decryptionkey(x):
    l0 = x[:64]
    r0 = x[64:]
    k1 = xor2(l0,r0)
    dec_key = r0+k1
    return dec_key
#main
print()
print("---------------Improving Data Security Using Lightweight Cryptography--------------");print();print()
print(">>>>> Initial key generation <<<<< ");print()
x1,x2 = kcbingenerator()
print("Encryption key 128-bit (Kc) : ",x1)
print("Decryption key 128-bit (Ks) : ",x2);print()
print(">>>>>  Key Generation  <<<<<");print()
dk = decryptionkey(x2)
EncryptionRoundKeys = keygenerator(x1)
DecKeys = keygenerator(dk)
for i in range(len(EncryptionRoundKeys)):
    print("Encryption Round", i+1, " Key : ",EncryptionRoundKeys[i])
print()
DecryptionRoundKeys = []
DecryptionRoundKeys.append(DecKeys[4])
DecryptionRoundKeys.append(DecKeys[1])
DecryptionRoundKeys.append(DecKeys[0])
DecryptionRoundKeys.append(DecKeys[3])
DecryptionRoundKeys.append(DecKeys[2])
for i in range(len(DecKeys)):
    print("Decryption Round", i+1, " Key : ",DecryptionRoundKeys[i])