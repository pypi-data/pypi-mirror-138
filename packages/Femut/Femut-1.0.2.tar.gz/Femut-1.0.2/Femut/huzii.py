def huzii(Length, Sex='Male' or 'Female'):
    if Sex == 'Male' and Length > 0:
        result = (2.47 * (Length*10) + 549.01)/10
    elif Sex == 'Female' and Length > 0:
        result = (2.24 * (Length*10) + 610.43)/10
    else :
        pass
    return result