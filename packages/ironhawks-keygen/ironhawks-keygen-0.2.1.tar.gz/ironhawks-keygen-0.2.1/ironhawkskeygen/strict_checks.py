'''
Includes respective strict checking functions for 3rd to 6th strategies.
'''


from string import punctuation


def strict_check_3(password):
    if any(map(str.isalpha, password)) and any(map(str.isdigit, password)):
        return True
    return False


def strict_check_4(password):
    if (
        any(map(str.isalpha, password))
        and any(ch in punctuation for ch in password)
    ):
        return True
    return False


def strict_check_5(password):
    if (
        any(map(str.isdigit, password))
        and any(ch in punctuation for ch in password)
    ):
        return True
    return False


def strict_check_6(password):
    if (
        any(map(str.isalpha, password))
        and any(map(str.isdigit, password))
        and any(ch in punctuation for ch in password)
    ):
        return True
    return False


strict_checks_list = [
    strict_check_3, strict_check_4, strict_check_5, strict_check_6
]