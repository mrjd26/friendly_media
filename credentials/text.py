def find_first(inputs):
    mt= []

    first_nonrepeat = False
    
    for char in inputs:
        mt.append(char)

    for char in inputs:
        count=mt.count(char)

        if count == 1:
            return char
            first_nonrepeat = True

    if first_nonrepeat == False:
        return ""

print find_first('')
