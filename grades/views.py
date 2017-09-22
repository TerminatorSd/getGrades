# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import base64

from django.http import HttpResponse
from django.shortcuts import render
from grades.models import User

# import KevinHeader as kh

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
        return render(request, "postPage.html", {'error': 0})
    if (request.method == "POST"):
        print "android/ post"

        # extract feature of images in a certain folder and write them to the files
        # base_dir = '/home/xsd/Deep_Learning/Python_code/images'
        # feature_path = '/home/xsd/Deep_Learning/Python_code/feature'
        # pair_path = '/home/xsd/Deep_Learning/Python_code/pair.txt'
        # pair = kh.extract_feature(base_dir, feature_path)
        #
        # kh.write_pair(pair, pair_path)
        # #
        # pair_read = kh.read_from_pair(pair_path)

        # # extract feature of the image to be retrieve
        # image = '/home/xsd/Deep_Learning/Python_code/images/feiji.jpg'
        # image_path = '/home/xsd/Deep_Learning/Python_code/images'
        # code = kh.extract_feature_of_target(image)
        #
        # # # calculate the hamming distance of features
        # result = kh.calculate_hamming_distance(feature_path, code, 3)
        #
        # for j in result:
        #     print result[j]['name']
        #     name = pair_read[result[j]['name'].encode('utf-8')]
        #     print name
        #
        #     # encode*************encode***************encode***********
        #     res = os.path.join(image_path, name.decode('utf-8'))
        #
        #     print res


        return HttpResponse({'ok'})
        # return HttpResponse(json.dumps(pair_read))

def getImage(request):
    # f = open(r'/home/xsd/Deep_Learning/Python_code/images/feiji.jpg', 'rb')
    # ls_f = base64.b64encode(f.read())
    # f.close()

    image_data = open("/home/xsd/Deep_Learning/Python_code/images/feiji.jpg", "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")


