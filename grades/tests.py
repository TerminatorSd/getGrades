# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

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

print getHamming('1010', '0101')

