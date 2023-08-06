__author__ = """samrand majnooni"""
__email__ = 'sammajnoni@gamil.com'

#import libraries
from .codemelli import validator, generator, lookup
import random

#generate man first name

def randomBoyName():
    with open('./name_boy.txt',encoding="utf8") as f:
        words = f.read().split()
        my_pick = random.choice(words)
        return my_pick

    
#generate girl first name

    def randomGirlName():
        with open('./name_girl.txt',encoding="utf8") as f:
            words = f.read().split()
            my_lname = random.choice(words)
            return my_lname

#generate lastname

def randomLastName():
    with open('./last_name.txt',encoding="utf8") as f:
        words = f.read().split()
        my_lname = random.choice(words)
        return my_lname

#generate first name + lastname(boy)

def randomFullBoyName():
    return(randomBoyName()+' '+ randomLastName())

#generate first name + last name (girl)

def randomFullGirlName():
    return(randomGirlName() +' '+ randomLastName())

#generate random name(girl or boy)

def randomName():
    randomName=random.choice([randomFullGirlName(),randomFullBoyName()])
    return randomName

    
