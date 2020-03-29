#!/usr/bin/python
'''
Made as a "practice-project" with the help of Phue by  Nathanaël Lécaudé
A small Hue Api Library for python


hue-snek By Channel-42
'''

import json
import urllib3

#urllib Pool Manager is needed for http requests
http = urllib3.PoolManager()


class Light(object):
    """Light.
    Light object
    """
    def __init__(self, light_id, bridge):
        self.bridge = bridge
        self.light_id = light_id

        self._name = None
        self._brightness = None
        self._saturation = None
        self._hue = None
        self._state = None

    def __repr__(self):
        """__repr__.
        chenges the way how instace is represented
        """
        return f'<{self.__class__.__module__}.{self.__class__.__name__} object "{self.name}"'

    def get(self, *args):
        """get.
        Passthrough function for getting light info
        Args:
            args: (str type) e.g. "name", "on", "bri", etc. See Hue Api for all options
        """
        #linking to get_light function for internal class use
        return self.bridge.get_light(self.light_id, *args)

    def set(self, *args):
        """set.
        Passtrough function to set light properties
        Args:
            args: (str type) e.g. "on", "bri", "hue" (see Hue Api for all options)
        """
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


class Hue(object):
    """Hue.
    Main bridge object
    """
    def __init__(self, ip=None, user=None):
        self.ip = ip
        self.user = user
        self.address = f"{ip}/api/{user}/"

        self.light_id = {}
        self.light_name = {}
        self.light_modelid = {}
        self.light_object = {}

        self.group_all = {}
        self.group_name = {}
        self.group_type = {}

        self.scene_all = {}
        self.scene_name = {}
        self.scene_group = {}

    def checkup(self):
        """checkup.
        Checks connection to the bridge by doing a http request and then seeing if the API throws any error
        """
        #basic up check and username check
        try:
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
        except:
            return 1

    def req(self, mode='GET', address=None, data=None):
        """req.
        main request function for getting and setting data from the API
        Args:
            mode: 'GET' or 'PUT'
            address: The URL address of the request
            data: The data sent to the API. Only used if mode is 'PUT'.
        """
        #main request function for GET and PUT
        if address is None:
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
        """get_light.
        Gets light data and returns it as dict

        Args:
            light_id: Id of a light
            param: The Parameter that should be returned (e.g. "name", "on"). Leave unset if everything should be returned
        """
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
        """set_light.
        Sets a value of a light 
        Args:
            light_id: Target light's id
            param: Target parameter (see API for options)
            value: Desired value
        """
        #set light's parameter value based on light id using the req function
        if (light_id is None) or (param is None) or (value is None):
            return 1

        data = f'{{"{param}":{value}}}'
        lid = str(light_id)  #make sure light_id is string
        self.req('PUT', f'{self.address}lights/{lid}/state', data)
        return 0

    def get_lights(self, mode='obj'):
        """get_lights.
        Gets all lights listed in the API
        Args:
            mode: The infomration the function returns (str type: obj, id, name, modelid)
        """
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
        """get_group.
        Gets a groups and returns it as dict
        Args:
            group_id: The groups id
            param: The parameter that should be returned (leave unset if everything should be returned)
        """
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
        """set_group.
        Sets a parameter of a group
        Args:
            group_id: Target group's id
            param: Target parameter
            value: Desired value
        """
        #set group's parameter value based on light id using the req function
        if (group_id is None) or (param is None) or (value is None):
            return 1

        data = f'{{"{param}":{value}}}'
        gid = str(group_id)  #make sure light_id is string
        self.req('PUT', f'{self.address}groups/{gid}/action', data)
        return 0

    def get_groups(self, mode='all'):
        """get_groups.
        Gets all groups listed in the API

        Args:
            mode: Changes return mode (str type: all, name, type)
        """
        #gets all groups based on selected mode (standard is all mode) and returns dict
        groups = self.req('GET', f'{self.address}groups')

        for group, val in groups.items():
            self.group_all[int(group)] = val
            self.group_name[int(group)] = val['name']
            self.group_type[int(group)] = val['type']

        if mode == "all":
            return self.group_all
        if mode == "name":
            return self.group_name
        if mode == "type":
            return self.group_type

    def get_scenes(self, mode='all'):
        """get_scenes.
        Gets all scenes listed in the API
        Args:
            mode: Changes return mode (str type: all, name, group)
        """
        #gets all scenes based on selected mode (standard is all mode) and returns dict
        scenes = self.req('GET', f'{self.address}scenes')

        for scene, val in scenes.items():
            self.scene_all[str(scene)] = val
            self.scene_name[str(scene)] = val['name']
            self.scene_group[str(scene)] = val.get(
                "group")  #using ["group] raises a KeyError

        if mode == "all":
            return self.scene_all
        if mode == "name":
            return self.scene_name
        if mode == "group":
            return self.scene_group

    def set_scene(self, group_id=1, scene_name=None):
        """set_scene.
        Sets a scene for a specified groub (by id)

        Args:
            group_id: Target group's id
            scene_name: Desired scene
        """
        #sets a scene for specific group based on scene name
        scenes = self.get_scenes("name")

        if scene_name in scenes.values():
            #get scene id from given name
            scene_id = list(scenes.keys())[list(
                scenes.values()).index(scene_name)]
            data = f'{{"scene":"{scene_id}"}}'
            #set scene for group
            self.req("PUT", f'{self.address}groups/{group_id}/action', data)

    def get_bridge_info(self):
        """get_bridge_info.
        Returns bridge's name, id, mac-address, model-id and api-version as dict
        """
        #returns dict with bridge info
        info = self.req('GET', f'{self.address}config')
        params = ['name', 'brideid', 'mac', 'modelid', 'apiversion']

        ret = {}

        #only add the above params to the return dict
        for param, val in info.items():
            if param in params:
                ret[param] = val

        return ret
