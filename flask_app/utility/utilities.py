
#checks if a string has an uppercase character or not
def has_uppercase(string):
    for char in string:
        if char.isupper():
            return True
    return False


#checks if a string has one number or not
def has_number(string):
    for char in string:
        if char.isnumeric():
            return True
    return False
