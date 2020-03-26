# hue_snek [WIP]
> A python Library for the Philips Hue API

<div size="100%">
<img align="center" border="0" padding="4" src="https://github.com/channel-42/hue-snek/blob/master/.resources/snek.png" width="50%">
</div>

# About
hue_snek is a python library for the Philips Hue API, that allows for easy API integration into other projects. The goal of this library is to provide the basic functions needed to interact with the Hue API, without unecessary functions.  

I will add more documentation and progress reports in the following days since the projects is still very bare bones at the moment.

# Features

- connect to bridge
- get light information (name, state, modelname, etc.)
- set light parameters  (on/off, brightness, hue, etc.)
- get group information (name, on/off, colormode, etc.)
- set group parameters  (on/off, brightness, hue, etc.)

# WIP

- add get_groups() funktion, to get all groups (similar to get_lights())
-

# Example

Basic usage of this library.

> Note that at the moment the hue_snek.py file has to be in the same directory as your script or in pythons path. You could also append the system path at the beginning of you file with `import sys` and then `sys.path.append('path/to/file')`, then `import hue_snek`.

```python
from hue_snek import hue, Light

#setup bridge
h = hue('192.168.178.20', 'generic-username')

#to check the connection to the bridge use:
h.checkup()  #returns 0 if connection and username OK

#to get Light information use either the Light or Hue class

#Light
Light(1, h).name
Light(1, h).brightness

#Hue
h.get_light(2, 'name')  #parameters: see hue api
h.get_lights('id')  #modes: obj (standard), id, name, modelid

h.get_group(1, 'name')  #parameters: see hue api

#to set lights or groups use either the Light or Hue Class

#Light
Light(2, h).set('bri', '124')

#Hue
h.set_light(1, 'on', 'true')

h.set_group(1, 'on', 'true')

```
# Notes

This project was inspired by ![Phue](https://github.com/studioimaginaire/phue/). Check it out :)
