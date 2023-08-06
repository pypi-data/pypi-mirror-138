#!/usr/bin/env python
# coding: utf-8

# Copyright (c) nicolas allezard.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""


from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Bool, validate, TraitError,Int,List,Dict,Bytes
from ipywidgets.widgets.trait_types import (
    bytes_serialization,
    _color_names,
    _color_hex_re,
    _color_hexa_re,
    _color_rgbhsl_re,
)
from ._frontend import module_name, module_version


import numpy as np
import base64
import cv2
import copy
def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    return img

def writeb64(img):
    """Encode matrix to base64 image string"""
    retval, buffer = cv2.imencode('.png', img)
    pic_str = base64.b64encode(buffer)
    pic_str = pic_str.decode()
    return pic_str

@register
class ipypixano(DOMWidget, ValueWidget):
    _model_name = Unicode('PixanoModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _view_name = Unicode('PixanoView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    pixano_element=Unicode('pxn-rectangle').tag(sync=True)
    image_path=Unicode('').tag(sync=True)
    image_data= Unicode('').tag(sync=True) #Bytes(default_value=None, allow_none=True).tag(sync=True, **bytes_serialization)
    counter=Int(666).tag(sync=True)
    shapes=List([]).tag(sync=True)
    selectedShapeIds=List([]).tag(sync=True)
    shapes_in=List([]).tag(sync=True)
    mask=Unicode('').tag(sync=True)


    def getMask(self):
        if self.mask!='':
            img=readb64(self.mask)
            return img
        else:
            return None

    def setImage(self,img):
        img_b64=writeb64(img)
        self.image_data=img_b64

    def setShapes(self,new_shape):
        self.shapes_in=copy.deepcopy(new_shape)