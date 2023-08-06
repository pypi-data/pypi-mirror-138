import base64
from hashlib import *
import hashlib
def login(usernameArray, passwordArray, inputUsername, Inputpassword):
    if usernameArray.__contains__(inputUsername):
        uan = usernameArray.index(inputUsername)
        if usernameArray[uan] == inputUsername:
            unc = True
        else: unc = False
    else: unc = False
    if passwordArray.__contains__(Inputpassword):
        pan = passwordArray.index(Inputpassword)
        if passwordArray[pan] == Inputpassword:
            pwc = True
        else: pwc = False
    else: pwc = False
    if pwc:
        if unc:
            if uan == pan:
                return True 
            else: return False
        else: return False
    else: return False

class secure:
    class b64:
        def encrypt(input):
            encrypted = base64.b64encode(input.encode('utf-8'))
            print(encrypted)
            return(encrypted)
        def encodeArray(inputArray):
            encrypted = []
            for i in inputArray:
                i = i.encode('utf-8')
                encrypted.append(base64.b64encode(i))
            return(encrypted)

        def login(usernameArray, HashedpasswordArray, inputUsername, inputpassword):     
            Hashedinputpassword = base64.b64encode(inputpassword.encode('utf-8'))
            if usernameArray.__contains__(inputUsername):
                uan = usernameArray.index(inputUsername)
                if usernameArray[uan] == inputUsername:
                    unc = True
                else: unc = False
            else: unc = False
            if HashedpasswordArray.__contains__(Hashedinputpassword):
                pan = HashedpasswordArray.index(Hashedinputpassword)
                if HashedpasswordArray[pan] == Hashedinputpassword:
                    pwc = True
                else: pwc = False
            else: pwc = False
            if pwc:
                if unc:
                    if uan == pan:
                        return True 
                    else: return False
                else: return False
            else: return False
    
    class sha256:
        def hash(input):
            hashed = hashlib.sha256(input.encode('utf-8')).hexdigest()
            print(hashed)
            return(hashed)
        def hasharray(inputArray):
            hashed = []
            for i in inputArray:
                i = i.encode('utf-8')
                hashed.append(hashlib.sha256(i).hexdigest())
            return(hashed)

        def login(usernameArray, HashedpasswordArray, inputUsername, inputpassword):     
            Hashedinputpassword = hashlib.sha256(inputpassword.encode('utf-8')).hexdigest()
            if usernameArray.__contains__(inputUsername):
                uan = usernameArray.index(inputUsername)
                if usernameArray[uan] == inputUsername:
                    unc = True
                else: unc = False
            else: unc = False
            if HashedpasswordArray.__contains__(Hashedinputpassword):
                pan = HashedpasswordArray.index(Hashedinputpassword)
                if HashedpasswordArray[pan] == Hashedinputpassword:
                    pwc = True
                else: pwc = False
            else: pwc = False
            if pwc:
                if unc:
                    if uan == pan:
                        return True 
                    else: return False
                else: return False
            else: return False
