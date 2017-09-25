# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import random

# Create your tests here.
# -*- coding: utf-8 -*-

def getHamming(a, b):
    dif = 0
    if(len(a) == len(b)):
        for i in range(len(a)):
            if(a[i] != b[i]):
                dif += 1
        return dif

    else:
        return "Error: len(a)!=len(b)!"

def getRandomFeature():
    feature = ""
    for i in range(1, 1000):
        ran = random.random()
        if(ran > 0.5):
            feature += '1'
        else:
            feature += '0'

    return feature

print getHamming('1010', '0101')
print getRandomFeature()
