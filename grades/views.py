# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponse
from django.shortcuts import render
from grades.models import User

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
        postData = request.POST
        print postData
        return HttpResponse({'ok'})


