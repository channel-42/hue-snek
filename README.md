# hue_snek [WIP]
> A python Library for the Philips Hue API

<img align="left" border="0" padding="4" src="https://github.com/channel-42/hue-snek/blob/master/.resources/snek.png" width="50%">

# About
hue_snek is a python library for the Philips Hue API, that allows for easy API integration into other projects.

I will add more documentation and progress reports in the following days since the projects is still very bare bones at the moment.

# Features

- get light information (name, state, modelname, etc.)
- set light parameter (on/off, brightness, hue)
- connect to bridge

# WIP

- add parameter control
- basically finish most of the base code: Light class, hue class functions
- Light class properties
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

```
# Notes

This project was inspired by ![Phue](https://github.com/studioimaginaire/phue/). Check it out :)
