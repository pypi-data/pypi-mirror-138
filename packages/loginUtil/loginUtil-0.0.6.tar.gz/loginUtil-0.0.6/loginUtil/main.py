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