def check_similar(string1, string2):
    string1=string1.replace("."," ")
    string2=string2.replace("."," ")

    string2=string2.lower()
    string1=string1.lower()

    string2=string2.split()
    string1=string1.split()

    if string1[0][0]!=string2[0][0]:
        return False

    d=len(string2)
    e=len(string1)

    if d>3:
        return False

    if e>3:
        return False

    a=string2.pop()
    b=string1.pop()

    if a==b:
        a=string1
        b=string2

    if(a[0]==b[0]):
        return True

    if (len(a)==2 and len(b)==1) or (len(a)==1 and len(b)==2):
        if a[0] in b[0]:
            return True
        elif b[0] in a[0]:
            return True
        else:
            return False
    elif (len(a)==1 and len(b)==1) or (len(a)==2 and len(b)==2):
        if a[0] in b[0]:
            return True
        elif b[0] in a[0]:
            return True
        else:
            return False
    else:
        return False
