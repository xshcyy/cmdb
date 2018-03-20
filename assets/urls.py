#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#date:2018-02-28
#function:

__author__ = 'xiaoshouhua'

from django.conf.urls import url
from assets import views

app_name = 'assets'

urlpatterns = [
    url(r'^report/', views.report, name='report'),
]
