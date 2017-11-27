import pandas as Reader
import xlrd
import numpy as pd
import matplotlib

theWorkbook = Reader.ExcelFile('../Data Files/WatsonConvGen Excel Template.xlsx')
theSettings = Reader.read_excel(theWorkbook, sheetname=None)
theValues = theSettings['Settings']
theData = theValues.loc[:, "WorkspaceName"]
theData2 = theData.values
for _ in theData2:
    print(_)
