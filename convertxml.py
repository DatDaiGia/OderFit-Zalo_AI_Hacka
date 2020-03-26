# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 09:51:56 2019

@author: pham.van.toan
"""

import cv2
import numpy as np
import xml.etree.cElementTree as ET
import xml
import os

XML_TRAIN_FD = "xmls/"
TRAIN_FD = "images/"
def gen_xml_files(img_fp, labels, save_xml_fd=XML_TRAIN_FD):
    img_fn = img_fp.split("/")[-1].split(".")[0]
    img = cv2.imread(img_fp)[:, :, ::-1]

    try:
        labels = np.array(labels.split(' ')).reshape(-1, 5)
    except AttributeError:
        return None

    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = TRAIN_FD
    ET.SubElement(root, "filename").text = img_fn + ".jpg"
    ET.SubElement(root, "path").text = os.path.join(TRAIN_FD, img_fn) + ".jpg"

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(root, "size")
    height, width, depth = img.shape
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    ET.SubElement(root, "segmented").text = "0"

    for codepoint, x, y, w, h in labels:
        xmin, ymin, w, h = int(x), int(y), int(w), int(h)
        xmax = xmin + w
        ymax = ymin + h

        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = "kuzu"
        ET.SubElement(obj, "pose").text = 'Unspecified'
        ET.SubElement(obj, "truncated").text = '0'
        ET.SubElement(obj, "difficult").text = '0'

        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(xmin)
        ET.SubElement(bbox, "ymin").text = str(ymin)
        ET.SubElement(bbox, "xmax").text = str(xmax)
        ET.SubElement(bbox, "ymax").text = str(ymax)

    xml_str = ET.tostring(root).decode("utf-8")
    xml_indent = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="\t")
    new_fn = "{}.xml".format(img_fn)
    new_fn = os.path.join(save_xml_fd, new_fn)
    with open(new_fn, "w") as f:
        f.write(xml_indent)     
        
