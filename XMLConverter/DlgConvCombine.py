# -*- coding: utf-8 -*-

# Author: Tuzeeky
# Date  : 05/10/2018

# Convert and combine ENG/CHS M*.txt and Q*.txt exported by GJDSE.exe
# and their translated version into to xlsx format.
# You need to install xlsxwriter (http://xlsxwriter.readthedocs.io)
# before running this script
# Put translated TXT under ENG folder and raw Chinese TXT under CHS folder

# The xlsx will have 6 columns 
# ID | Character | CHS | ENG Character | ENG | ENG REV

# This script was written under Python 3.6.2
# Usage: python DlgTXTImporter.py <TXTFilename>


import ntpath
import sys
import os
import xlsxwriter

def addTranslatedEntry(txt, dict):
    for line in txt:
        lineStr = line.decode('utf_8').strip()
        sections = lineStr.split("\t")

        if (len(sections) == 3 and len(sections[0]) > 0): # leave out the "splitter" lines
            dict[sections[0].replace(u'\ufeff', '')] = (sections[1], sections[2]) 

    return

def main(argv):
    if len(sys.argv) <= 1:
        print('Please specify the TXT file name!!\n')
        print('Usage: python DlgConvCombine.py <Filename>\n')
        return

    txtFilename = sys.argv[1]

    try:
        txtFileCHS = open('CHS/' + txtFilename, 'rb')
    except IOError:
        print ('Could not open CHS/' + txtFilename + ' to read from!')
        return
    
    try:
        txtFileENG = open('ENG/' + txtFilename, 'rb')
    except IOError:
        print ('Could not open ENG/' + txtFilename + ' to read from!')
        return

    translatedDict = {}
    addTranslatedEntry(txtFileENG, translatedDict)

    sheetName = os.path.splitext(ntpath.basename(txtFilename))[0]
    outFileName = sheetName + '.xlsx';
    workbook = xlsxwriter.Workbook(outFileName)
    worksheet = workbook.add_worksheet(sheetName)

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'ID', bold)
    worksheet.write('B1', 'Character', bold)
    worksheet.write('C1', 'CHS', bold)
    worksheet.write('D1', 'ENG Character', bold)
    worksheet.write('E1', 'ENG', bold)
    worksheet.write('F1', 'ENG REV', bold)

    defaultColumnWidth = 80
    worksheet.set_column(2, 2, defaultColumnWidth) 
    worksheet.set_column(4, 5, defaultColumnWidth) 

    row = 2
    for line in txtFileCHS:
        lineStr = line.decode('utf_8').strip()
        sections = lineStr.split("\t")

        if (len(sections) == 3 and len(sections[0]) > 0): # leave out the "splitter" lines
            cell_format = workbook.add_format()
            cell_format.set_text_wrap()

            id = sections[0].replace(u'\ufeff', '')
            worksheet.write('A' + str(row),  id, cell_format) # index. Remove \ufeff at beginning
            worksheet.write('B' + str(row),  sections[1], cell_format) # character name
            worksheet.write('C' + str(row),  sections[2], cell_format) # dialogue content

            if (id in translatedDict):
                entry = translatedDict[id]
                worksheet.write('D' + str(row),  entry[0], cell_format) # dialogue content
                worksheet.write('E' + str(row),  entry[1], cell_format) # dialogue content

            row+=1

        else:
            print("Skip line: ", end="")
            for section in sections:
                print(section + '\t', end="")
            print("If this line is not a splitter line, please double check it has correct format in TXT!\nEach column needs to be separated by ONE TAB\n")

    workbook.close()
    print('Exported to ' + outFileName + ' successfully!')
    return

if __name__ == "__main__":
    main(sys.argv)