# -*- coding: utf-8 -*-

# Import M*.txt and Q*.txt to table.data.
# This script only support importing SeqDlg at the moment.
# If you want to import other table, change tableName below.

# This script was written under Python 3.6.2
# Put this script under the same directory with data.table and GJDSEC.exe
# Usage: python SeqDlgTXTImporter.py <TXTFilename>

# !!! THE TXT FILE HAS TO BE ENCODED IN UTF-8-BOM
# !!!!!! You must use ONE TAB to separate each columns. Otherwise parsing will fail.

import os
import sys
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def main(argv):
    if len(sys.argv) <= 1:
        print('Please specify the TXT file name!!\n')
        print('Usage: python SeqDlgTXTImporter.py <TXTFilename>\n')
        return

    txtFilename = sys.argv[1]
    tableFilename = 'data.table'
    xmlFilename = 'Request.xml'

    try:
        txtFile = open(txtFilename, 'rb')
    except IOError:
        print ('Could not open ' + txtFilename + ' to read from!')
        return

    xmlRoot = Element('Request')
    tree = ElementTree(xmlRoot)
    tableName = 'SeqDlg' + os.path.splitext(txtFilename)[0]

    for line in txtFile:
        lineStr = line.decode('utf_8')
        sections = lineStr.split("\t")
        if (len(sections) == 3 and len(sections[0]) > 0): # leave out the "splitter" lines
            FCO3 = sections[0].replace(u'\ufeff', '') # index. Remove \ufeff at beginning
            DZ04 = sections[1] # character name
            DZ05 = sections[2] # dialogue content

            updateNodeAttrib = {u'Table':tableName, u'Where':'FCO3 = \'' + FCO3 + '\''}
            updateNode = SubElement(xmlRoot, u'Update', updateNodeAttrib)

            nameNodeAttrib = {u'Column':'DZ04'}
            nameNode = SubElement(updateNode, u'Value', nameNodeAttrib)
            nameNode.text = DZ04

            dialogNodeAttrib = {u'Column':u'DZ05'}
            dialogNode = SubElement(updateNode, u'Value', dialogNodeAttrib)
            dialogNode.text = DZ05
        else:
            print("Skip line: ", end="")
            for section in sections:
                print(section + '\t', end="")
            print("If this line is not a splitter line, please double check it has correct format in TXT!\nEach column needs to be separated by ONE TAB\n")
    try:
        xmlFile = open(xmlFilename, 'wb')
    except IOError:
        print ('Could not open ' + xmlFilename + ' to write to!')
        return

    xmlFile.write(u'<?xml version="1.0" encoding="utf-8" ?>\n'.encode(encoding='utf_8'))
    tree.write(xmlFile)

    txtFile.close()
    xmlFile.close()

    os.system('GJDSEC.exe -f ' + tableFilename + ' -x ' + xmlFilename) # Invoke GJDSEC.exe to import data from XML
    os.remove(xmlFilename) # Comment out this line to see the generated XML file

    print ('\n\nFinished importing ' + txtFilename)

    return

if __name__ == "__main__":
    main(sys.argv)
