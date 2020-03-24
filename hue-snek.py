#!/usr/bin/python

import json
import os
import sys
import urllib3

http = urllib3.PoolManager()

class Light(object):

    def __init__(self, state, bridge):
        self.state = state
        self.bridge = bridge
        
        self.id
        self.name
        self.brightness
        self.saturation
        self.hue

    def __repr__(self):
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object "{self.name}"'
            

class hue(object):

    def __init__(self, ip=None, user=None):
        self.ip = ip
        self.user = user
        self.address = f"{ip}/api/{user}/"

    def checkup(self):
        api = http.request('GET', self.address)
        #check for http connection
        if api.status != 200:
            return 1
        
        js = json.loads(api.data.decode('utf-8'))
        #check for api error 
        try:
            if js[0]['error']:
                return js[0]['error']['description']
        except:
            pass
            return 0
    
    def req(self, mode='GET', address=None, data=None):
        if address == None:
            address = self.address
        try:
            
            if mode == 'GET':
                ret = json.loads(http.request(mode, address).data.decode('utf-8)'))
                return ret 
        
            if (mode == 'POST') or (mode == 'PUT'):
                http.request(mode, address, body=data, headers={'Content-Type': 'application/json'})
                return 0 
        except:
            return 1
    

print(hue("http://192.168.178.75", "O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I").req('PUT', 'http://192.168.178.75/api/O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I/lights/1/state', '{"on":false}'))

#print(hue("http://192.168.178.75", "O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I").req('GET', 'http://192.168.178.75/api/O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I/lights/1'))
