def pearson(Length, Sex='Male' or 'Female'):
    if Sex == 'Male' and Length > 0:
        result = 81.306 + 1.880 * Length
    elif Sex == 'Female' and Length > 0:
        result = 72.844 + 1.945 * Length
    else :
        pass
    return result