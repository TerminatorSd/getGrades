# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import requests
from lxml import etree

def index(request):
    return render(request, 'index.html')

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
        # print content
        content = etree.HTML(content)
        name = content.xpath("//p/span/text()")[0]
        result = content.xpath("//table/tr[@class='t_con']/td/text()")

        ret = {}
        i = 0
        ret[str(i)] = name
        i += 1
        for res in result:
            st = str(i)
            i += 1
            res = res.strip()
            if(res):
                ret[st] = res

        # return render(request, 'grades.html', {'grades': ret})
        return HttpResponse(json.dumps(ret))


