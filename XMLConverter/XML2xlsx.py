# -*- coding: utf-8 -*-

# Author: Tuzeeky
# Date  : 05/15/2018

# Convert xml format text file exported by GJDSEC.exe
# to xlsx format.
# You need to install xlsxwriter (http://xlsxwriter.readthedocs.io)
# before running this script

# This script was written under Python 3.6.2
# Usage: python XML2xlsx.py <TXTFilename>

import ntpath
import os
import sys
import xlsxwriter
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree, parse

def getColumn(title, dict, currColumn):
    new = False
    if (title not in dict):
        dict[title] = currColumn
        currColumn = chr(ord(currColumn) + 1)  # can't really handle Z + 1, but meh we don't have so many columns so whatever
        new = True
    return dict[title], currColumn, new

def writeCell(title, row, format, value, sheet, itemColumeDict, currColumn):
    cellColumn, currColumn, isNew = getColumn(title, itemColumeDict, currColumn)
    cellIndex = cellColumn + str(row)
    if (isNew or row == 1):
        titleIndex = cellColumn + '1'
        sheet.write(titleIndex, title, format)
    if (row != 1):
        sheet.write(cellIndex, value, format)
    return cellColumn, currColumn

def XML2xlsx(sourceFilename, dictEng = None, dictEngRev = None):
    srcXML = parse(sourceFilename)
    srcXMLRoot = srcXML.getroot()
    tableRoot = srcXMLRoot.find('Select')  
    
    sheetName = os.path.splitext(ntpath.basename(sourceFilename))[0]
    outFileName = sheetName + '.xlsx';
    workbook = xlsxwriter.Workbook(outFileName)
    worksheet = workbook.add_worksheet(sheetName)

    column = 'A'
    row = 2
    rowPerItem = 4
    itemColumeDict = {}

    warpFormat = workbook.add_format()
    warpFormat.set_text_wrap()
    boldFormat = workbook.add_format({'bold': True})
    cellColumn, column = writeCell('LANG', 1, boldFormat, 'LANG', worksheet, itemColumeDict, column)

    dictColumnMaxWidth = {}
    
    for item in tableRoot:
        cellColumn, column = writeCell('LANG', row, warpFormat, 'CHS', worksheet, itemColumeDict, column)
        cellColumn, column = writeCell('LANG', row + 1, warpFormat, 'ENG', worksheet, itemColumeDict, column)
        cellColumn, column = writeCell('LANG', row + 2, warpFormat, 'ENG REV', worksheet, itemColumeDict, column)

        childrenCount = len(item.getchildren())
        titleColumnName = item[0].get('Column')

        cellColumn, column = writeCell(titleColumnName, row, warpFormat, item[0].text, worksheet, itemColumeDict, column)
        cellColumn, column = writeCell(titleColumnName, row + 1, warpFormat, item[0].text, worksheet, itemColumeDict, column)
        cellColumn, column = writeCell(titleColumnName, row + 2, warpFormat, item[0].text, worksheet, itemColumeDict, column)

        itemDictEng = None
        itemDictEngRev = None

        if (dictEng is not None):
            itemDictEng = dictEng[item[0].text]

        if (dictEngRev is not None):
            itemDictEngRev = dictEng[item[0].text]

        for i in range(1, childrenCount):
            itemColumnId = item[i].get('Column')
            itemValue = item[i].text
            if (itemValue is None):
                itemValue = ''
            cellColumn, column = writeCell(itemColumnId, row, warpFormat, itemValue, worksheet, itemColumeDict, column)
            strWidth = min(80, len(itemValue) * 2)
            if (strWidth > dictColumnMaxWidth.get(cellColumn, 0)):
                dictColumnMaxWidth[cellColumn] = strWidth
            
            if (itemDictEng is not None):
                if (itemColumnId in itemDictEng):
                    engVal = itemDictEng[itemColumnId]
                    cellColumn, column = writeCell(itemColumnId, row + 1, warpFormat, engVal, worksheet, itemColumeDict, column)

            if (itemDictEngRev is not None):
                if (itemColumnId in itemDictEngRev):
                    engRevVal = itemDictEngRev[itemColumnId]
                    cellColumn, column = writeCell(itemColumnId, row + 2, warpFormat, engRevVal, worksheet, itemColumeDict, column)    

        row += rowPerItem

    for col, width in dictColumnMaxWidth.items():
        worksheet.set_column(col + ':' + col, width)
    
    workbook.close()
    print('Exported to ' + outFileName + ' successfully!')
    return
  
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Please specify the TXT/XML file name!!\n')
        print('Usage: python XML2xlsx.py <XMLFilename>\n')
    else:
        XML2xlsx(sys.argv[1])