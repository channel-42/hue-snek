#!/usr/bin/python
'''
Made as a "practice-project" with the help of Phue by  Nathanaël Lécaudé
A small Hue Api Library for python

Light class:
    - missing properties: saturation, hue, state (on/off)

hue-snek By Channel-42
'''

import json
import os
import sys
import urllib3

#urllib Pool Manager is needed for http requests
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
        #change how instances are represented
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object "{self.name}"'

    def get(self, *args):
        #linking to get_light function for internal class use
        return self.bridge.get_light(self.light_id, *args)

    def set(self, *args):
        #link to set_light function for internal class use
        return self.bridge.set_light(self.light_id, *args)

    #get and set properties of light object (name, brightness, etc.)

    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, value):
        self._name = value
        self.set('name', self._name)

    @property
    def brightness(self):
        self._brightness = self.get('bri')
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self.set('bri', self._brightness)

    @property
    def saturation(self):
        return self.get('sat')

    @saturation.setter
    def saturation(self):
        self._saturation = self.get('sat')
        return self._saturation

    @property
    def hue(self):
        return self.get('hue')

    @hue.setter
    def hue(self):
        self._hue = self.get('hue')
        return self._hue

    @property
    def state(self):
        return self.get('on')

    @state.setter
    def state(self):
        self._state = self.get('on')
        return self._state


class hue(object):
    def __init__(self, ip=None, user=None):
        self.ip = ip
        self.user = user
        self.address = f"{ip}/api/{user}/"
        self.light_id = {}
        self.light_name = {}
        self.light_modelid = {}
        self.light_object = {}

    def checkup(self):
        #basic up check and username check
        api = http.request('GET', self.address)

        #check for http connection
        if api.status != 200:
            return 1

        js = json.loads(api.data.decode('utf-8'))

        #check for api error (eg wrong username)
        try:
            if js[0]['error']:
                return js[0]['error']['description']
        except:
            pass
            return 0

    def req(self, mode='GET', address=None, data=None):
        #main request function for GET and PUT
        if address == None:
            address = self.address  #use standard adress (see __init__)
        try:
            #get request
            if mode == 'GET':
                ret = json.loads(
                    http.request(mode, address).data.decode('utf-8)'))
                return dict(ret)
            #put request (body and header needed for urllib3)
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

        lid = str(light_id)  #make sure light id is string
        state = self.req('GET', f'{self.address}lights/{lid}')  #make request

        if param is None:
            return state  #return whole light state page

        #check if parameter is in main body or in state subbody (see json structure)
        if param in ['name', 'modelid', 'type', 'productname', 'productid']:
            return state[param]
        else:
            return state['state'][param]

    def set_light(self, light_id=None, param=None, value=None):
        #set light's parameter value based on light id using the req function
        if (light_id is None) or (param is None) or (value is None):
            return 1

        data = f'{{"{param}":{value}}}'
        lid = str(light_id)  #make sure light_id is string
        self.req('PUT', f'{self.address}lights/{lid}/state', data)
        return 0

    def get_lights(self, mode='obj'):
        #gets all lights based on selected mode (standard is object mode) and returns dict
        lights = self.req('GET', f'{self.address}lights')

        for light, val in lights.items():
            self.light_object[int(light)] = Light(int(light), self)
            self.light_id[int(light)] = Light(int(light), self).light_id
            self.light_name[int(light)] = val['name']
            self.light_modelid[int(light)] = val['modelid']

        if mode == 'obj':
            return self.light_object
        if mode == "id":
            return self.light_id
        if mode == "name":
            return self.light_name
        if mode == "modelid":
            return self.light_modelid

    def get_group(self, group_id=None, param=None):
        #gets group info
        if group_id is None:
            return 1

        gid = str(group_id)  #make sure group id is string
        state = self.req('GET', f'{self.address}groups/{gid}')  #make request

        if param is None:
            return state  #return whole group state page

        #check if parameter is in main body or in state subbody (see json structure)
        if param in ['name', 'colormode', 'type', 'alert', 'lights']:
            return state[param]
        else:
            return state['action'][param]

    def set_group(self, group_id=None, param=None, value=None):
        #set group's parameter value based on light id using the req function
        if (group_id is None) or (param is None) or (value is None):
            return 1

        data = f'{{"{param}":{value}}}'
        gid = str(group_id)  #make sure light_id is string
        self.req('PUT', f'{self.address}groups/{gid}/action', data)
        return 0
