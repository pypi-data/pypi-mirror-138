'''
IronHawks KeyGen: Example v0.2.1

An example file to showcase keygen.py functionality with a nice output 
latency.

Created by Praveen K. Contact: hartbrkrlegacy@gmail.com
'''


import logging
import sys
import time

logging.basicConfig(level=logging.INFO, 
                    format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

import keygen


STRATEGIES = {
    1 : "Generate using Alphabets only.",
    2 : "Generate using Digits only.",
    3 : "Generate using Alphabets and Digits only.",
    4 : "Generate using Alphabets and Special Characters only.",
    5 : "Generate using Digits and Special Characters only.",
    6 : "Generate using Alphabets, Digits and Special Characters."
}


def show_strategies():
    logger.info("Choose one of the following options to generate a password:")
    for i in range(1,7):
        logger.info(str(i) + ". " + str(STRATEGIES[i]))
    logger.info("0. Exit.")


def get_strategy():
    try:
        choice = int(input("Enter the corresponding option's number(0-6): "))
        if choice < 0 or choice > 6:
            raise ValueError()
        if choice == 0:
            sys.exit("Exited.")
        return choice
    except ValueError:
        logger.error("Invalid input! Enter a number between 0 to 6.", 
                     exc_info=True)
        return get_strategy()
    

def get_length():
    try:
        length = int(input("Enter the preferred length of the password: "))
        if length == 0:
            sys.exit("Exited.")
        if length < 8 or length > 128:
            raise ValueError()
        return length
    except ValueError:
        logger.error("""Invalid input! Enter a number between 8 to 128 or 0 to 
exit.""", exc_info=True)
        return get_length()


def get_strict():
    try:
        strict = str(input("Enable Strict mode? (True/False): "))
        if strict not in ["True", "False"]:
            raise ValueError()
        return strict == "True"
    except ValueError:
        logger.error("""Invalid input! Enter either True or False.""", 
                     exc_info=True)
        return get_strict()

if __name__ == '__main__':
    logger.info(__doc__)
    show_strategies()
    strategy_number = get_strategy()

    logger.info('''Accepted. In the following prompt, enter the preferred 
length of the password. Minimum is 8 and Maximum is 128. Recommended length is 
12 to 15 characters.''')
    password_length = get_length()

    logger.info('''Accepted. In the following prompt, enter True to enable 
Strict mode() or False to disable it. Any other input except True or False will
 lead to prompting again. Refer docs for "Strict" mode.''')
    strict = get_strict()

    logger.info('''Accepted. Generating a password with strategy: '{}', length:
 {} and strict: {}...'''.format(
    str(STRATEGIES[strategy_number]), str(password_length), str(strict)
    ))

    generated_password = keygen.generate(strategy_number, password_length, 
                                         strict=strict)
    
    time.sleep(2)
    logger.info("Password generation successful!")
    logger.info("Generated Password: {}".format(generated_password))
    time.sleep(2)
    logger.info("Exited.")