"""getGrades2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from grades import views as grades_views

urlpatterns = [
    url(r'^index/', grades_views.grades),
    url(r'^grades/', grades_views.grades),
    url(r'^getGrades/', grades_views.getGrades, name = "grades"),
    url(r'^login/', grades_views.login),
    url(r'^register/', grades_views.register, name = "register"),
    url(r'^newUser/', grades_views.newUser, name="newUser"),
    url(r'^userLogin/', grades_views.userLogin),
    url(r'^admin/', admin.site.urls),

    url(r'^android/', grades_views.androidTest),
    url(r'^getImage/', grades_views.getImage),
    url(r'^android_2/', grades_views.android_image),
    url(r'^squeeze/', grades_views.squeezeNet),
    url(r'^queryAll/', grades_views.queryAll),
    url(r'^forSim/', grades_views.forSimilarity)
]
