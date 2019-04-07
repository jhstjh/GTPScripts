# -*- coding: utf-8 -*-

# Author: Tuzeeky
# Date  : 05/21/2018

# Combine CHS/ENG xml format text file exported by GJDSEC.exe
# to one xlsx format.
# You need to install xlsxwriter (http://xlsxwriter.readthedocs.io)
# and XML2xlsx.py
# before running this script

# This script was written under Python 3.6.2
# Usage: python XML2xlsx.py <TXTFilename>

import ntpath
import os
import sys
import xlsxwriter
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree, parse

import XML2xlsx

def combine(sourceFilename):
    chsFile = 'CHS/' + sourceFilename
    engFile = 'ENG/' + sourceFilename

    engXML = parse(engFile)
    engXMLRoot = engXML.getroot()
    tableRoot = engXMLRoot.find('Select')  
    engDict = {}

    for item in tableRoot:
        itemDict = {}
        id = item[0].text
        childrenCount = len(item.getchildren())
        for i in range(1, childrenCount):
            itemColumnId = item[i].get('Column')
            itemValue = item[i].text
            itemDict[itemColumnId] = itemValue
        engDict[id] = itemDict

    XML2xlsx.XML2xlsx(chsFile, engDict)

  
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Please specify the TXT/XML file name!!\n')
        print('Usage: python XML2xlsx.py <XMLFilename>\n')
    else:
        combine(sys.argv[1])