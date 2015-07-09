# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

class Page(object):
    
    title = None
    active = False

    def __init__(self, title, active):
        self.title = title
        self.active = active 

