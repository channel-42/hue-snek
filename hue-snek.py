#!/usr/bin/python
'''
Made as a "practice-project" with the help of Phue by  Nathanaël Lécaudé
A small Hue Api Library for python

hue-snek By Channel-42
'''

import json
import os
import sys
import urllib3

http = urllib3.PoolManager()


class Light(object):
    def __init__(self, light_id, bridge):
        self.bridge = bridge
        self.light_id = light_id

        self._name = None
        self._brightness = None
        self._saturation = None
        self._hue = None
        self._state = None

    def __repr__(self):
        #change how isinstances are represented
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object "{self.name}"'

    def get(self, *args):
        #linking to get_light function for internal class use
        return self.bridge.get_light(self.light_id, *args)

    def set(self, *args):
        #link to set_light function for internal class use
        return self.bridge.set_light(self.light_id, *args)

    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self._name = value


class hue(object):
    def __init__(self, ip=None, user=None):
        self.ip = ip
        self.user = user
        self.address = f"{ip}/api/{user}/"
        self.light_id = {}
        self.light_name = {}
        self.light_modelid = {}

    def checkup(self):  #basic up check and username check
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
        #main request function for GET and PUT
        if address == None:
            address = self.address
        try:

            if mode == 'GET':
                ret = json.loads(
                    http.request(mode, address).data.decode('utf-8)'))
                return dict(ret)

            if (mode == 'POST') or (mode == 'PUT'):
                http.request(mode,
                             address,
                             body=data,
                             headers={'Content-Type': 'application/json'})
                return 0
        except:
            return 1

    def get_light(self, light_id=None, param=None):
        #get light info
        if light_id is None:
            return 1

        lid = str(light_id)
        state = self.req('GET', f'{self.address}lights/{lid}')

        if param is None:
            return state

        if param in ['name', 'modelid', 'type', 'productname', 'productid']:
            return state[param]

    def set_light(self, light_id=None, param=None, value=None):
        #set light's parameter value based on light id
        if (light_id is None) or (param is None) or (value is None):
            return 1
        data = f'{{"{param}":{value}}}'
        print(data)
        lid = str(light_id)
        self.req('PUT', f'{self.address}lights/{lid}/state', data)
        print(f'{self.address}lights/{lid}/state')

    def get_lights(self, mode=None):
        #gets all lights (WIP: CHANGE TO LIGHT OBJECT INSTEAD OF LIST!!)
        lights = self.req('GET', f'{self.address}lights')

        for light, val in lights.items():
            self.light_id[int(light)] = light
            self.light_name[int(light)] = val['name']
            self.light_modelid[int(light)] = val['modelid']

        if mode == "id":
            return self.light_id
        if mode == "name":
            return self.light_name
        if mode == "modelid":
            return self.light_modelid


h = hue("http://192.168.178.75", "O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I")

print(Light(1, h).name)
#print(hue("http://192.168.178.75", "O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I").req('GET', 'http://192.168.178.75/api/O4qAaBl9LaXonrNlAu0Pzei3ianWAJuUzYuZpC2I/lights/1'))
