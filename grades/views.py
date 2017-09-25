# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import time

from django.http import HttpResponse
from django.shortcuts import render
from grades.models import User
from grades.models import featureMap as fm

import KevinHeader as kh
import SqueezeHeader as sh

# Create your views here.
import requests
from lxml import etree

def grades(request):
    return render(request, 'grades.html')

def login(request):
    return render(request, 'login.html', {'error':0})

def register(request):
    return render(request, 'register.html', {'error':0})

# 添加新用户
def newUser(request):
    if(request.method == "POST"):
        postData = request.POST
        acc = postData.get('account')
        psw = postData.get('password')
        result = User.objects.filter(account = acc)
        if(result):
            return render(request, 'register.html', {'error':1})
        else:
            User.objects.create(account = acc, password = psw)
            return render(request, 'login.html')


# 用户登录
def userLogin(request):
    if(request.method == "POST"):
        postData = request.POST
        acc = postData.get('account')

        result = User.objects.filter(account = acc)
        print result
        if(result):
            return render(request, "grades.html")
        else:
            return render(request, "login.html",{'error':1})

# 查询成绩
def getGrades(request):
    print "enter getGrades()"
    if (request.method == "POST"):
        postData = request.POST
        account = postData.get('no')
        password = postData.get('psw')
        loginURL = r'https://cas.scut.edu.cn/amserver/UI/Login'
        postData = {
            "IDToken0": "",
            "IDToken1": account,
            "IDToken2": password,
            "IDButton": "Submit",
            "goto": "aHR0cDovL3lqc2p5LjF5ZDMuY2FzLnNjdXQuZWR1LmNuL3NzZncval9zcHJpbmdfaWRzX3NlY3VyaXR5X2NoZWNr",
            "encoded": "true",
            "inputCode": "",
            "gx_charset": "UTF-8",
        }
        session = requests.Session()
        session.post(loginURL, data=postData)
        text = session.get("http://yjsjy.1yd3.cas.scut.edu.cn/ssfw/pygl/cjgl/cjcx.do")
        content = text.content
        content = etree.HTML(content)
        ret = {}
        try:
            name = content.xpath("//p/span/text()")[0]
            result = content.xpath("//table/tr[@class='t_con']/td/text()")
            i = 0
            ret[str(i)] = name
            i += 1
            for res in result:
                st = str(i)
                i += 1
                res = res.strip()
                if (res):
                    ret[st] = res
        except:
            ret = ""
        # return render(request, 'grades.html', {'grades': ret})
        return HttpResponse(json.dumps(ret))


def androidTest(request):
    print "enter androidTest()"
    if (request.method == "GET"):
        return render(request, "success.html", {'error': 0})
    if (request.method == "POST"):
        print "android/ post"
        return HttpResponse({'ok'})


def getImage(request):
    # f = open(r'/home/xsd/Deep_Learning/Python_code/images/feiji.jpg', 'rb')
    # ls_f = base64.b64encode(f.read())
    # f.close()

    if(request.method == "GET"):

        data = request.GET

        img = data.get('name')

        path = "/home/xsd/Deep_Learning/Python_code/images/" + img

        image_data = open(path, "rb").read()

        # print image_data
        return HttpResponse(image_data, content_type="image/jpg")



def android_image(request):
    print "enter android_image()"
    if (request.method == "GET"):
        return render(request, "postPage.html", {'error': 0})
    if (request.method == "POST"):
        print "android/ post"

        # extract feature of images in a certain folder and write them to the database
        base_dir = '/home/xsd/Deep_Learning/Python_code/images'
        feature_path = '/home/xsd/Deep_Learning/Python_code/feature'

        # pair contains imageName, textName and feature_code
        pair = kh.extract_feature(base_dir, feature_path)

        time1 = time.time()

        for item in pair:
            # print item,
            # print item.encode('utf-8')
            result = fm.objects.filter(imageName=item)
            if(result):
                result.feature = pair[item]['code']
            else:
                fm.objects.create(imageName=item, textName=pair[item]['txt_name'], feature=pair[item]['code'])

        return HttpResponse(json.dumps(pair))

def squeezeNet(request):
    print "enter squeezeNet..."
    if (request.method == "GET"):
        return render(request, "postPage.html", {'error': 0})
    if (request.method == "POST"):
        print "squeeze/post..."

        # extract feature of images in a certain folder and write them to the database
        base_dir = '/home/xsd/Deep_Learning/Python_code/images'
        feature_path = '/home/xsd/Deep_Learning/Python_code/feature'

        # pair contains imageName, textName and feature_code
        pair = sh.extract_feature(base_dir, feature_path)

        time1 = time.time()

        for item in pair:
            # print item,
            # print item.encode('utf-8')
            result = fm.objects.filter(imageName=item)
            if (result):
                result.update(feature = pair[item]['code'])
                # result.values().feature = pair[item]['code']
            else:
                fm.objects.create(imageName=item, textName=pair[item]['txt_name'], feature=pair[item]['code'])

        print time.time()-time1

        return HttpResponse(json.dumps(pair))


def queryAll(request):
    if (request.method == "POST"):

        pair = {}
        res = fm.objects.all().values()

        for item in res:
            pair[item['imageName']] = item['feature']

        print pair
        return HttpResponse(json.dumps(pair))

def forSimilarity(request):
    print "Enter forSimilarity..."
    feature = sh.getRandomFeature()
    feature = '1111111111111101110111111000000111111000111110110001001000001111001011000000000011111110110111100100000111110000110001000000000000000110101111101110001100100111001000000001111000111010111110001101101101010001100100000010000101010011100111001010010011100110000100111000111111111111111111111111110110110000000000000000000110100011001111011111111110011110111111111011100011111111111111111001011110110100000000000000101000110000000000010011001000010000000011100100000110000110110100100000010100001010000001101110100011111001000000010100101001010001010001001000100000110010000010010000000010011000010011101001001100010100001110110000000011001111000100000000000000110000101000000110110011001000100001001000100000000011100110010111011010001000000000100000111001110010110101010100111000100011110000000000110100001101111101001000000000010000000111010100111011111001000111010100000000011010000101000000000011010110110001101000111001000000000000000100000000011010011011000000100010000101011000000001001010011011'

    if(request.method == "POST"):

        print "enter forSim/post..."
        postData = request.POST
        pair = {}
        res = fm.objects.all().values()

        for item in res:
            pair[item['imageName']] = sh.getHamming(feature, item['feature'])

        pair_sort = sorted(pair.iteritems(), key=lambda asd: asd[1], reverse=False)

        result = sh.printTopk(3, pair_sort)

        return HttpResponse(json.dumps(result))