# hue_snek [![](https://img.shields.io/badge/version-0.2-green.svg)](https://pypi.org/project/hue-snek-channel42/)  [![Downloads](https://pepy.tech/badge/hue-snek-channel42)](https://pepy.tech/project/hue-snek-channel42)  ![](https://img.shields.io/badge/license-MIT-orange.svg) 
> A python Library for the Philips Hue API

<p align="center">
    <img src="https://repository-images.githubusercontent.com/249658807/1eee5080-78e5-11ea-8abd-4c3bee68e521" width="70%">
</p>


## About
hue_snek is a python library for the Philips Hue API, that allows for easy API integration into other projects. The goal of this library is to provide the basic functions needed to interact with the Hue API, without unnecessary functions.  

This API library was made as a practice project and is no longer in active development.

## Installation

`pip install hue-snek-channel42`

## Features

- connect to bridge
- get light information (name, state, modelname, etc.)
- set light parameters  (on/off, brightness, hue, etc.)
- get group information (name, on/off, colormode, etc.)
- set group parameters  (on/off, brightness, hue, etc.)
- get scene information (name, assigned group(s), etc.)
- set scene for group   (via scene name)
- get bridge information (name, mac, api-version, etc.)

## hue_snek in action
<img align="right" src="https://repository-images.githubusercontent.com/250581922/d2d0ce00-7775-11ea-9377-7a3b3d153045" width="50%">

An example of what can theoretically accomplished with hue_snek is [huetui](https://github.com/channel-42/hue-tui), which is a TUI for controlling Hue lights.

<br>
Another possible implementation would be a CLI, which would have more scripting potential than a TUI.
<br>
<br>
<br>
<br>

## Example Usage

Basic usage of this library:


```python
from hue_snek_pkg.hue_snek import Hue, Light

#setup bridge
h = Hue('your.ip.here', 'your-username')

#to check the connection to the bridge use:
h.checkup()                     #returns 0 if connection and username OK

#to get Light information use either the Light or Hue class

#Light
Light(1, h).name                #(light id, bridge)
Light(1, h).brightness          #properties: name, brightness, hue, saturation, state

#Hue
h.get_light(2, 'name')          #parameters: see hue api
h.get_lights('id')              #modes: obj (default, id, name, modelid

h.get_group(1, 'name')          #parameters: see hue api
h.get_groups('name')            #modes: all (default), name, type


#to set lights or groups use either the Light or Hue Class

#Light
Light(2, h).set('bri', '124')

#Hue
h.set_light(1, 'on', 'true')

h.set_group(1, 'on', 'true')

#scenes can be accessed and set like this:

h.get_scenes('name')            #modes: all (default), name, group
h.set_scene(1, 'Chill')         #(group id, scene name)

info = h.get_bridge_info()

for param, value in info.items():
    print(param, value)

```
## Notes

This project was inspired by [Phue](https://github.com/studioimaginaire/phue/). 
